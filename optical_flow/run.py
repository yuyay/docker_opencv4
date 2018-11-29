import cv2
import numpy as np 
import time

def read_and_preprocess_image(file):
    im = cv2.imread(file)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    return gray

def flow_to_img(raw_flow, bound):
    '''
    this function scale the input pixels to 0-255 with bi-bound
    :param raw_flow: input raw pixel value (not in 0-255)
    :param bound: upper and lower bound (-bound, bound)
    :return: pixel value scale from 0 to 255
    '''
    flow = raw_flow
    flow[flow > bound] = bound
    flow[flow < -bound] = -bound
    flow += bound
    flow *= 255 / (2 * bound)
    return flow


if __name__ == "__main__":
    im1 = read_and_preprocess_image("sample1.jpg")
    im2 = read_and_preprocess_image("sample2.jpg")

    # Calculate flow
    start = time.time() 
    optflow = cv2.optflow.DualTVL1OpticalFlow_create()
    flow = optflow.calc(im1, im2, None)
    elapsed = time.time() - start
    print("Calculation time: {0:.4f} sec. ({1:.2f} fps)".format(
        elapsed, 1.0 / elapsed))

    # Save flow as image
    flow_x = flow_to_img(flow[..., 0], 15)
    flow_y = flow_to_img(flow[..., 1], 15)
    cv2.imwrite("flow_x.jpg", flow_x)
    cv2.imwrite("flow_y.jpg", flow_y)
