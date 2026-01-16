
```sql
-- Example values (replace with actual)
SET @hotel_id         = 123;
SET @new_template_id  = 7;          -- the template we want to switch TO
SET @now              = NOW();      -- or use application-provided timestamp

START TRANSACTION;

-- 1. Mark the CURRENT template as deactivated (if any exists)
UPDATE HotelTemplates
SET 
    deactivated_on = @now
WHERE 
    hotel_id       = @hotel_id
    AND deactivated_on IS NULL;     -- only the currently active one has NULL

-- 2. Make sure we have a row for the NEW template
--    (either insert new or update if it was used before and deactivated)
INSERT INTO HotelTemplates (
    hotel_id,
    template_id,
    activated_on,
    deactivated_on
)
VALUES (
    @hotel_id,
    @new_template_id,
    @now,
    NULL
)
ON DUPLICATE KEY UPDATE
    -- If the hotel used this template before → reactivate it
    activated_on   = @now,
    deactivated_on = NULL;

-- 3. Update the official current pointer in Hotels table
UPDATE Hotels
SET current_template_id = @new_template_id
WHERE id = @hotel_id;

COMMIT;
```

COALESCE -> Give me the hotel value if it exists, otherwise give me the template value.

```sql
-- Example: Get content for a specific hotel page + section
-- (this is the most important query pattern you'll need)

SELECT 
    COALESCE(
        hsh.heading_text,
        tsh.heading_text
    ) AS effective_heading,
    
    COALESCE(
        hsd.description_text,
        tsd.description_text
    ) AS effective_description,
    
    COALESCE(
        hsi.image_url,
        tsi.image_url
    ) AS effective_image_url,

    -- You can also add flags if helpful
    CASE WHEN hsh.id IS NOT NULL THEN 'custom' ELSE 'template_default' END AS source_heading,
    CASE WHEN hsd.id IS NOT NULL THEN 'custom' ELSE 'template_default' END AS source_description

FROM HotelPages hp
JOIN TemplatePages tp ON tp.id = hp.template_page_id

LEFT JOIN HotelSections hs 
    ON hs.hotel_page_id = hp.id
LEFT JOIN TemplatePageSections tps 
    ON tps.template_page_id = tp.id
    AND tps.template_section_id = hs.template_section_id   -- match by logical section

LEFT JOIN HotelSectionHeadings hsh ON hsh.hotel_section_id = hs.id
    AND hsh.order_index = 1   -- or whatever position you're interested in
LEFT JOIN TemplateSectionHeadings tsh 
    ON tsh.template_page_section_id = tps.id
    AND tsh.order_index = 1

LEFT JOIN HotelSectionDescriptions hsd ON hsd.hotel_section_id = hs.id
LEFT JOIN TemplateSectionDescriptions tsd ON tsd.template_page_section_id = tps.id

LEFT JOIN HotelSectionImages hsi ON hsi.hotel_section_id = hs.id
    AND hsi.order_index = 1
LEFT JOIN TemplateSectionImages tsi ON tsi.template_page_section_id = tps.id
    AND tsi.order_index = 1

WHERE 
    hp.hotel_id = 123
    AND tp.page_name = 'home'          -- or whatever page
    AND hs.is_active = 1
ORDER BY COALESCE(hs.order_index, tps.order_index);
```