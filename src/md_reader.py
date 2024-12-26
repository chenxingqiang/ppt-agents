import markdown
from bs4 import BeautifulSoup
from markdown.extensions.tables import TableExtension


class MarkdownReader:
    def __init__(self, markdown_path):
        self.markdown_path = markdown_path
        self.references = []  # Store all references
        self.ref_counter = 1  # Counter for reference numbering
        with open(markdown_path, "r", encoding="utf-8") as file:
            self.md_content = file.read()
        # Enable table extension and other useful extensions
        self.html_content = markdown.markdown(
            self.md_content,
            extensions=[
                'tables',
                'footnotes',
                'attr_list',
                'def_list',
                'fenced_code',
            ]
        )
        self.soup = BeautifulSoup(self.html_content, "html.parser")

    def _add_reference(self, ref_text):
        """Add a reference and return its number."""
        if ref_text not in self.references:
            self.references.append(ref_text)
            ref_num = self.ref_counter
            self.ref_counter += 1
            return ref_num
        return self.references.index(ref_text) + 1

    def _process_references_section(self, elem):
        """Process a references section and return numbered references."""
        refs = []
        current_ref = []
        seen_urls = set()  # Track seen URLs to avoid duplicates
        
        for p in elem.find_all("p"):
            # Skip empty paragraphs
            if not p.text.strip():
                continue
                
            # Process each link in the paragraph
            for content in p.contents:
                if content.name == "a":
                    link_text = content.text.strip()
                    href = content.get("href", "").strip()
                    
                    # Skip if we've seen this URL before
                    if href in seen_urls:
                        continue
                    
                    # Handle PDF links
                    if link_text.startswith("[PDF]"):
                        continue
                    
                    if href and link_text:
                        seen_urls.add(href)
                        ref_text = f"{link_text} ({href})"
                        ref_num = self._add_reference(ref_text)
                        refs.append(f"[{ref_num}] {ref_text}")
                elif isinstance(content, str):
                    text = content.strip()
                    if text and not text.startswith("[[PDF]"):
                        current_ref.append(text)
            
            # Add any non-link text as a reference if it exists
            if current_ref:
                ref_text = " ".join(current_ref).strip()
                if ref_text:
                    ref_num = self._add_reference(ref_text)
                    refs.append(f"[{ref_num}] {ref_text}")
                current_ref = []
        
        return refs

    def _process_paragraph(self, elem):
        """Process a paragraph or list item, handling links and formatting."""
        text_parts = []
        seen_urls = set()  # Track seen URLs to avoid duplicates
        
        for content in elem.contents:
            if content.name == "a":
                link_text = content.text.strip()
                href = content.get("href", "").strip()
                
                # Skip if we've seen this URL before
                if href in seen_urls:
                    continue
                    
                # Handle PDF links
                if link_text.startswith("[PDF]"):
                    continue
                
                if href and link_text:
                    seen_urls.add(href)
                    ref_text = f"{link_text} ({href})"
                    ref_num = self._add_reference(ref_text)
                    text_parts.append(f"{link_text} [{ref_num}]")
            elif isinstance(content, str):
                # Handle plain text, but skip PDF markers
                text = content.strip()
                if text and not text.startswith("[[PDF]"):
                    text_parts.append(text)
            else:
                # Handle other elements (strong, em, code)
                text = content.text.strip()
                if text:
                    text_parts.append(text)
        
        return " ".join(text_parts).strip()

    def get_title(self):
        title = self.soup.find("h1")
        return title.text if title else ""

    def get_subtitle(self):
        subtitle = self.soup.find("h2")
        return subtitle.text if subtitle else ""

    def get_sections(self):
        """Get all sections from the markdown content."""
        sections = []
        current_section = None
        current_content = []
        current_references = []

        for elem in self.soup.find_all(["h1", "h2", "h3", "p", "ul", "table"]):
            if elem.name in ["h1", "h2", "h3"]:
                # Save previous section if it exists
                if current_section:
                    current_section["content"] = current_content
                    current_section["references"] = current_references
                    sections.append(current_section)
                    current_content = []
                    current_references = []

                # Start new section
                current_section = {
                    "title": elem.text.strip(),
                    "content": [],
                    "references": []
                }
            elif elem.name == "p":
                # Check if this paragraph contains references
                if "重要参考文献" in elem.text:
                    # Skip this paragraph as it's just a header
                    continue
                
                # Process the paragraph
                text = self._process_paragraph(elem)
                if text:
                    # Check if this is a reference
                    if any(ref_marker in text.lower() for ref_marker in ["参考文献", "reference", "引用"]):
                        current_references.extend(self._process_references_section(elem))
                    else:
                        current_content.append({
                            "type": "text",
                            "data": text
                        })
            elif elem.name == "ul":
                # Process list items
                items = [self._process_paragraph(li) for li in elem.find_all("li")]
                items = [item for item in items if item]  # Remove empty items
                if items:
                    current_content.append({
                        "type": "list",
                        "data": items
                    })
            elif elem.name == "table":
                # Process table
                table_data = self._process_table(elem)
                if table_data:
                    current_content.append({
                        "type": "table",
                        "data": table_data
                    })

        # Add the last section
        if current_section:
            current_section["content"] = current_content
            current_section["references"] = current_references
            sections.append(current_section)

        return sections

    def _process_table(self, table_elem):
        """Process a table element into a structured format."""
        table_data = {
            "headers": [],
            "rows": []
        }
        
        # Process headers
        header_row = table_elem.find("thead")
        if header_row:
            headers = header_row.find_all("th")
            table_data["headers"] = [h.text.strip() for h in headers]
        
        # Process rows
        body = table_elem.find("tbody")
        if body:
            for row in body.find_all("tr"):
                row_data = [cell.text.strip() for cell in row.find_all("td")]
                if any(row_data):  # Only add non-empty rows
                    table_data["rows"].append(row_data)
        
        return table_data if table_data["rows"] else None