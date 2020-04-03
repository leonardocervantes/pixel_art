import sys
import cv2 
import numpy as np

# # Notes:
# B G R 
B = 0
G = 1
R = 2

def process(img, pxl):
    wdth = img.shape[0]
    hght = img.shape[1]

    pxl_sz = np.size(pxl, 0)
    print("width: ", wdth)
    print("height: ", hght)
    
    col_sz  = int(wdth/pxl_sz)
    row_sz =  int(hght/pxl_sz)

    print("col size: ", col_sz)
    print("row size: ", row_sz)

    start_col = int(wdth/2 - (col_sz*(pxl_sz/2)))
    start_row = int(hght/2 - (row_sz*(pxl_sz/2)))

    for j in range(pxl_sz):
        for i in range(pxl_sz):
            begin_col = start_col + col_sz*j
            end_col = begin_col + col_sz

            begin_row = start_row + row_sz*i
            end_row = begin_row + row_sz 

            sub_mat_b = img[begin_col:end_col , begin_row:end_row, B]
            sub_mat_g = img[begin_col:end_col , begin_row:end_row, G]
            sub_mat_r = img[begin_col:end_col , begin_row:end_row, R]
           
            b = np.average(sub_mat_b)
            g = np.average(sub_mat_g)
            r = np.average(sub_mat_r)
            
            pxl[j, i, B] = b
            pxl[j, i, G] = g
            pxl[j, i, R] = r
    return

def blowup(pxl_smol, pxl_big, scale, bits):
    for i in range(bits):
        for j in range(bits):
            
            b = pxl_smol[i, j, B]
            g = pxl_smol[i, j, G]
            r = pxl_smol[i, j, R]
            row_start = i*scale
            row_end = i*scale + scale - 1

            col_start = j*scale
            col_end = j*scale + scale - 1

            pxl_big[row_start:row_end, col_start:col_end, B] = b
            pxl_big[row_start:row_end, col_start:col_end, G] = g
            pxl_big[row_start:row_end, col_start:col_end, R] = r
    return



def convert_image(file, bits):
    # open the image file
    img = cv2.imread(file)
    
    # create bitxbit image
    pxl = np.zeros((bits, bits, 3), np.uint8)

    # process image, average and put into new image
    process(img, pxl)

    # turn 32x32 to 640x640
    scale = 20
    pxl_big = np.zeros((bits*scale, bits*scale, 3), np.uint8)
    blowup(pxl, pxl_big, scale, bits)

    # write to file
    # 'in/image_name.png' -> image_name
    file_name = file.split('/')[1].split('.')[0]
    pixel_file = "out/{}.jpg".format(file_name)

    cv2.imwrite(pixel_file, pxl_big)
    return

if __name__ == "__main__":

    if "-animal" in sys.argv:
        bits = 32

    if len(sys.argv) < 2:
        print("Need a file")
        sys.exit()
    
    image_file = sys.argv[1]

    convert_image(image_file, bits)