import PySimpleGUI as sg
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
from io import BytesIO

#sg.theme('DarkBrown')
#sg.theme('Reddit')
sg.theme('LightGreen')

# Function to update the displayed image based on applied filters
def update_image(original, blur, contrast, brightness, sharpness, emboss, contour, flipx, flipy, sepia, grayscale):
    global image
    image = original.filter(ImageFilter.GaussianBlur(blur))
    image = image.filter(ImageFilter.UnsharpMask(contrast))
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness)
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(sharpness)

    if emboss:
            image = image.filter(ImageFilter.EMBOSS())
    if contour:
            image = image.filter(ImageFilter.CONTOUR())
    if flipx:
            image = ImageOps.mirror(image)
    if flipy:
            image = ImageOps.flip(image)
    if sepia:
        image = sepia_filter(image)
    if grayscale:
        image = grayscale_filter(image)
        
    # Convert the updated image to PNG format and update the displayed image
    bio = BytesIO()
    image.save(bio, format = 'PNG')
    window['-IMAGE-'].update(data = bio.getvalue())

def sepia_filter(img):
    sepia_filter = Image.new('RGB', img.size)
    sepia_filter.paste(ImageOps.colorize(img.convert('L'), (170, 82, 45), (255, 215, 0)), (0, 0, img.width, img.height))
    return sepia_filter

def grayscale_filter(img):
    return ImageOps.grayscale(img)

#image_path = 'image_editor/tree.png'
image_path = sg.popup_get_file('Open', no_window=True)

# Define the layout with control columns and displayed image column
control_col = sg.Column([
    [sg.Frame('Blur', font=('Bodoni MT', 17), layout = [[sg.Slider(range=(0, 10), orientation='h', key='-BLUR-', size=(25, 20))]])],
    [sg.Frame('Contrast', font=('Bodoni MT', 17), layout = [[sg.Slider(range=(0, 10), orientation='h', key='-CONTRAST-', size=(25, 20))]])], 
    [sg.Frame('Brightness', font=('Bodoni MT', 17), layout=[[sg.Slider(range=(0.1, 2.0), default_value=1.0, orientation='h', resolution=0.1, key='-BRIGHTNESS-', size=(25, 20))]])],
    [sg.Frame('Sharpness', font=('Bodoni MT', 17), layout=[[sg.Slider(range=(0, 10), orientation='h', key='-SHARPNESS-', size=(25, 20))]])],
    [sg.Checkbox('Emboss', key = '-EMBOSS-', font=('Bodoni MT', 17)), sg.Checkbox('Contour', key = '-CONTOUR-', font=('Bodoni MT', 17))],
    [sg.Checkbox('Flip x', key = '-FLIPX-', font=('Bodoni MT', 17)), sg.Checkbox('Flip y', key = '-FLIPY-', font=('Bodoni MT', 17))],
    [sg.Checkbox('Sepia', key='-SEPIA-', font=('Bodoni MT', 17)), sg.Checkbox('Grayscale', key='-GRAYSCALE-', font=('Bodoni MT', 17))],
    [sg.Button('Save image', key='-SAVE-', font=('Bodoni MT', 17))],
])
image_col = sg.Column([[sg.Image(image_path, key = '-IMAGE-')]])

layout = [[control_col, image_col]]

# Open the image and create a window to display the layout
original = Image.open(image_path)
window = sg.Window('Image Editor', layout)

# Event loop to handle user interactions
while True:
    event, values = window.read(timeout = 50)
    if event == sg.WIN_CLOSED:
        break

    update_image(original, 
                 values['-BLUR-'], 
                 values['-CONTRAST-'],
                 values['-BRIGHTNESS-'],
                 values['-SHARPNESS-'],
                 values['-EMBOSS-'], 
                 values['-CONTOUR-'], 
                 values['-FLIPX-'], 
                 values['-FLIPY-'], 
                 values['-SEPIA-'], 
                 values['-GRAYSCALE-'])
    
    if event == '-SAVE-':
        save_path = sg.popup_get_file('Save', save_as=True, no_window=True) + '.png'
        image.save(save_path, 'PNG')

window.close()