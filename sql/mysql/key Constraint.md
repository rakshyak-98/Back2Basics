```mysql
CREATE TABLE HotelSections (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hotel_template_id INT NOT NULL,
    template_section_id INT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (hotel_template_id) REFERENCES HotelTemplates(id),
    FOREIGN KEY (template_section_id) REFERENCES TemplateSections(id)
);

ALTER TABLE HotelSections
ADD CONSTRAINT unique_hotel_template_section UNIQUE (hotel_template_id, template_section_id);

```


**Create during table creation**
```mysql
CREATE TABLE HotelSections (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hotel_template_id INT NOT NULL,
    template_section_id INT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (hotel_template_id) REFERENCES HotelTemplates(id),
    FOREIGN KEY (template_section_id) REFERENCES TemplateSections(id),
    UNIQUE (hotel_template_id, template_section_id)
);

```