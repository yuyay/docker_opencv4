import cv2
import numpy as np 
import time
import argparse
import os
import glob
from joblib import Parallel, delayed
import tqdm

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


def process_one(prevfile, nextfile, bound):
    xout = nextfile.replace("rgb_", "flowx_")
    yout = nextfile.replace("rgb_", "flowy_")

    im1 = read_and_preprocess_image(prevfile)
    im2 = read_and_preprocess_image(nextfile)

    # Calculate flow
    optflow = cv2.optflow.DualTVL1OpticalFlow_create()
    flow = optflow.calc(im1, im2, None)

    # Save flow as image
    flow_x = flow_to_img(flow[..., 0], bound)
    flow_y = flow_to_img(flow[..., 1], bound)
    cv2.imwrite(xout, flow_x)
    cv2.imwrite(yout, flow_y)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-R', '--root', type=str, help="Root directory", required=True)
    parser.add_argument('-j', '--n-jobs', type=int, help="Number of parallel jobs", default=-1)
    parser.add_argument('-b', '--bound', type=float, help="Bound value for clipping", default=15)
    parser.add_argument('-s', '--stride', type=int, help="Stride", default=1)
    args = parser.parse_args()

    for dn in tqdm.tqdm(os.listdir(args.root)):
        files = glob.glob(os.path.join(args.root, dn, "rgb_*.jpg"))
        files = sorted(files)

        r = Parallel(n_jobs=args.n_jobs)([
            delayed(process_one)(files[i], files[i + 1], args.bound) for i in range(0, len(files) - 1, args.stride)
        ])
