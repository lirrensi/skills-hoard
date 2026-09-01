# PDF Forms

## Step 1: Check if Fillable

Run from this file's directory:
```bash
python scripts/check_fillable_fields <file.pdf>
```

## Fillable Forms

If the PDF has fillable fields:

1. **Extract field info**:
   ```bash
   python scripts/extract_form_field_info.py <input.pdf> field_info.json
   ```

2. **Convert to images for analysis**:
   ```bash
   python scripts/convert_pdf_to_images.py <file.pdf> <output_dir/>
   ```

3. **Create field_values.json**:
   ```json
   [
     {
       "field_id": "last_name",
       "page": 1,
       "value": "Simpson"
     },
     {
       "field_id": "Checkbox12",
       "page": 1,
       "value": "/On"
     }
   ]
   ```

4. **Fill the form**:
   ```bash
   python scripts/fill_fillable_fields.py <input.pdf> <field_values.json> <output.pdf>
   ```

## Non-Fillable Forms

If no fillable fields, use annotation approach:

1. **Extract structure** (try first):
   ```bash
   python scripts/extract_form_structure.py <input.pdf> form_structure.json
   ```

2. **Convert to images**:
   ```bash
   python scripts/convert_pdf_to_images.py <input.pdf> <images_dir/>
   ```

3. **Analyze and create fields.json** with coordinates (see PDF-basic.md for coordinate systems)

4. **Validate coordinates**:
   ```bash
   python scripts/check_bounding_boxes.py fields.json
   ```

5. **Fill with annotations**:
   ```bash
   python scripts/fill_pdf_form_with_annotations.py <input.pdf> fields.json <output.pdf>
   ```

6. **Verify output**:
   ```bash
   python scripts/convert_pdf_to_images.py <output.pdf> <verify_dir/>
   ```

## Coordinate Systems

- **PDF coordinates**: y=0 at bottom of page
- **Image coordinates**: y=0 at top of page
- Use `pdf_width`/`pdf_height` or `image_width`/`image_height` in JSON to specify system

## Important Notes

- Checkbox values: Use `/On` to check, or the field's `checked_value`
- Radio groups: Use values from `radio_options`
- Always validate bounding boxes before filling
