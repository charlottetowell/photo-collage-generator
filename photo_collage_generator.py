import os
from PIL import Image

def photo_collage_generator(
    input_folder='input',
    output_folder='output',
    dpi=300,
    card_width_inches=6,
    card_height_inches=4,
    grid_columns=2,
    grid_rows=1,
):

    ## Config stuff
    CARD_WIDTH_PX = card_width_inches * dpi
    CARD_HEIGHT_PX = card_height_inches * dpi
    PICS_PER_COLLAGE = grid_columns * grid_rows
    os.makedirs(output_folder, exist_ok=True)

    # load all the (image) files
    image_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder)
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    print(f"Found {len(image_files)} images in /{input_folder} to process")

    # group into collage sets
    collages = [image_files[i:i + PICS_PER_COLLAGE] for i in range(0, len(image_files), PICS_PER_COLLAGE)]
    total = len(collages)
    print(f"Generating {total} total collages...")

    def fit_image_to_box(im, box_size):
        """Resize and rotate the image to fit in the box without cropping."""
        w, h = im.size
        box_w, box_h = box_size

        # try normal
        ratio_normal = min(box_w / w, box_h / h)
        size_normal = (int(w * ratio_normal), int(h * ratio_normal))

        # try rotated
        ratio_rotated = min(box_w / h, box_h / w)
        size_rotated = (int(h * ratio_rotated), int(w * ratio_rotated))

        if size_rotated[0] * size_rotated[1] > size_normal[0] * size_normal[1]:
            im = im.rotate(90, expand=True)
            im = im.resize(size_rotated, Image.Resampling.LANCZOS)
        else:
            im = im.resize(size_normal, Image.Resampling.LANCZOS)

        return im

    # process collages
    for idx, collage in enumerate(collages):
        card = Image.new('RGB', (CARD_WIDTH_PX, CARD_HEIGHT_PX), 'white')

        for i, image_path in enumerate(collage):
            try:
                im = Image.open(image_path).convert('RGB')
            except Exception as e:
                print(f"\n\tError opening {image_path}: {e}, skipping")
                continue

            # define grid cell size
            cell_width = CARD_WIDTH_PX // grid_columns
            cell_height = CARD_HEIGHT_PX // grid_rows
            cell_box = (cell_width, cell_height)

            # position in grid
            row = i // grid_columns
            col = i % grid_columns

            fitted = fit_image_to_box(im, cell_box)

            # compute centered position within the grid cell
            x_offset = (col * cell_width) + (cell_width - fitted.width) // 2
            y_offset = (row * cell_height) + (cell_height - fitted.height) // 2

            card.paste(fitted, (x_offset, y_offset))

        # save result
        output_path = os.path.join(output_folder, f'pic_{idx + 1:03}.jpg')
        card.save(output_path, dpi=(dpi, dpi))

        print(f"\r\tSaved {idx + 1}/{total}", end='', flush=True)

    print("\nDone!")

if __name__ == "__main__":
    #config here
    INPUT_FOLDER = 'input'
    OUTPUT_FOLDER = 'output'
    DPI = 300
    CARD_WIDTH_INCHES = 6
    CARD_HEIGHT_INCHES = 4
    GRID_COLUMNS = 2
    GRID_ROWS = 1
    
    #run the generator
    photo_collage_generator(
        input_folder=INPUT_FOLDER,
        output_folder=OUTPUT_FOLDER,
        dpi=DPI,
        card_width_inches=CARD_WIDTH_INCHES,
        card_height_inches=CARD_HEIGHT_INCHES,
        grid_columns=GRID_COLUMNS,
        grid_rows=GRID_ROWS
    )
