"""
1. Write a function for RGB --> LAB
2. Write a function to proceed in DFS manner
3. Write a function for deltaE_1976(lab1, lab2)
4. Write a function to pick a point
"""

import os, sys
import numpy as np
from skimage import io, color
import matplotlib.pyplot as plt

def plotMinMax(Xsub_rgb,labels=["R","G","B"]):
    print("______________________________")
    for i, lab in enumerate(labels):
        mi = np.min(Xsub_rgb[:,:,i])
        ma = np.max(Xsub_rgb[:,:,i])
        print("{} : MIN={:8.4f}, MAX={:8.4f}".format(lab,mi,ma))

def deltaE(pt1, pt2):
    coord1 = img_lab[pt1[0]][pt1[1]]
    coord2 = img_lab[pt2[0]][pt2[1]]
    return np.sqrt( (coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2 + (coord1[2] - coord2[2])**2 )

def corner_pt(pt):
    if pt[0] == -1 : return 1
    if pt[1] == -1 : return 1
    if pt[0] == h  : return 1
    if pt[1] == w  : return 1
    return 0

def flood_fill3(pt):
    queue = []
    
    pt_start = list(pt)
    visited[pt[0]][pt[1]] = 1

    # Step 1 : loop over 8 neighbours for checking
    # --> not need for first point
    included[pt[0]][pt[1]] = 1

    # Step 2 : loop over 8 neighbours for adding to queue
    pt_left_x, pt_left_y = pt[0] - 1, pt[1]
    if not visited[pt_left_x][pt_left_y]:
        queue.append((pt_left_x, pt_left_y))
        visited[pt_left_x][pt_left_y] = 1

    pt_topleft_x, pt_topleft_y = pt[0] - 1, pt[1] + 1
    if not visited[pt_topleft_x][pt_topleft_y]:
        queue.append((pt_topleft_x, pt_topleft_y))
        visited[pt_topleft_x][pt_topleft_y] = 1

    pt_top_x, pt_top_y = pt[0], pt[1] + 1
    if not visited[pt_top_x][pt_top_y]:
        queue.append((pt_top_x, pt_top_y))
        visited[pt_top_x][pt_top_y] = 1

    pt_topright_x, pt_topright_y = pt[0] + 1, pt[1] + 1
    if not visited[pt_topright_x][pt_topright_y]:
        queue.append((pt_topright_x, pt_topright_y))
        visited[pt_topright_x][pt_topright_y] = 1

    pt_right_x, pt_right_y = pt[0] + 1, pt[1]
    if not visited[pt_right_x][pt_right_y]:
        queue.append((pt_right_x, pt_right_y))
        visited[pt_right_x][pt_right_y] = 1

    pt_bottomright_x, pt_bottomright_y = pt[0] + 1, pt[1] - 1
    if not visited[pt_bottomright_x][pt_bottomright_y]:
        queue.append((pt_bottomright_x, pt_bottomright_y))
        visited[pt_bottomright_x][pt_bottomright_y] = 1

    pt_bottom_x, pt_bottom_y = pt[0], pt[1] - 1
    if not visited[pt_bottom_x][pt_bottom_y]:
        queue.append((pt_bottom_x, pt_bottom_y))
        visited[pt_bottom_x][pt_bottom_y] = 1

    pt_bottomleft_x, pt_bottomleft_y = pt[0] - 1, pt[1] - 1
    if not visited[pt_bottomleft_x][pt_bottomleft_y]:
        queue.append((pt_bottomleft_x, pt_bottomleft_y))
        visited[pt_bottomleft_x][pt_bottomleft_y] = 1

    print (' -- Initial Queue : ', queue)
    iters = 0
    while len(queue):
        iters += 1
        if iters % 1000 == 0:
            pass
            # print (' -- Iters : ',iters, '||  Visited : ', np.unique(visited, return_counts = True), ' || Inlcluded : ', np.unique(included, return_counts = True))

        pt = list(queue.pop(0))
        visited[pt[0]][pt[1]] = 1

        # Step 1 : Loop over all 8 neigbours for checking
        pt_left_x, pt_left_y = pt[0] - 1, pt[1]
        if not corner_pt((pt_left_x, pt_left_y)):
            if included[pt_left_x][pt_left_y] and (not included[pt[0]][pt[1]]):
                diff     = deltaE(pt, (pt_left_x, pt_left_y))
                # diff     = deltaE()
                if diff <= thresh: 
                    included[pt[0]][pt[1]] = 1
            if not visited[pt_left_x][pt_left_y]:
                queue.append((pt_left_x, pt_left_y))
                visited[pt_left_x][pt_left_y] = 1
        
        pt_topleft_x, pt_topleft_y = pt[0] - 1, pt[1] + 1
        if not corner_pt((pt_topleft_x, pt_topleft_y)):
            if included[pt_topleft_x][pt_topleft_y] and (not included[pt[0]][pt[1]]):
                diff = deltaE(pt, (pt_topleft_x, pt_topleft_y))
                if diff <= thresh:
                    included[pt[0]][pt[1]] = 1
            if not visited[pt_topleft_x][pt_topleft_y]:
                queue.append((pt_topleft_x, pt_topleft_y))
                visited[pt_topleft_x][pt_topleft_y] = 1
        
        pt_top_x, pt_top_y = pt[0], pt[1] + 1
        if not corner_pt((pt_top_x, pt_top_y)):
            if included[pt_top_x][pt_top_y] and (not included[pt[0]][pt[1]]):
                diff = deltaE(pt, (pt_top_x, pt_top_y))
                if diff <= thresh:
                    included[pt[0]][pt[1]] = 1
            if not visited[pt_top_x][pt_top_y]:
                queue.append((pt_top_x, pt_top_y))
                visited[pt_top_x][pt_top_y] = 1


        pt_topright_x, pt_topright_y = pt[0] + 1, pt[1] + 1
        if not corner_pt((pt_topright_x, pt_topright_y)):
            if included[pt_topright_x][pt_topright_y] and (not included[pt[0]][pt[1]]):
                diff = deltaE(pt, (pt_topright_x, pt_topright_y))
                if diff <= thresh:
                    included[pt[0]][pt[1]] = 1
            if not visited[pt_topright_x][pt_topright_y]:
                queue.append((pt_topright_x, pt_topright_y))
                visited[pt_topright_x][pt_topright_y] = 1

        pt_right_x, pt_right_y = pt[0] + 1, pt[1]
        # if pt_right_x == pt_start[0] and pt_right_y == pt_start[1]:
        #     print (pt_right_x, pt_right_y, pt)
        #     print (included[pt_right_x][pt_right_y], included[pt[0]][pt[1]])
        #     print (included[pt_right_x][pt_right_y] and (not included[pt[0]][pt[1]]))
        if not corner_pt((pt_right_x, pt_right_y)):
            if included[pt_right_x][pt_right_y] and (not included[pt[0]][pt[1]]):
                diff = deltaE(pt, (pt_right_x, pt_right_y))
                if diff <= thresh:
                    included[pt[0]][pt[1]] = 1
            if not visited[pt_right_x][pt_right_y]:
                queue.append((pt_right_x, pt_right_y))
                visited[pt_right_x][pt_right_y] = 1

        pt_bottomright_x, pt_bottomright_y = pt[0] + 1, pt[1] - 1
        if not corner_pt((pt_bottomright_x, pt_bottomright_y)):
            if included[pt_bottomright_x][pt_bottomright_y] and (not included[pt[0]][pt[1]]):
                diff = deltaE(pt, (pt_bottomright_x, pt_bottomright_y))
                if diff <= thresh:
                    included[pt[0]][pt[1]] = 1
            if not visited[pt_bottomright_x][pt_bottomright_y]:
                queue.append((pt_bottomright_x, pt_bottomright_y))
                visited[pt_bottomright_x][pt_bottomright_y] = 1

        pt_bottom_x, pt_bottom_y = pt[0], pt[1] - 1
        if not corner_pt((pt_bottom_x, pt_bottom_y)):
            if included[pt_bottom_x][pt_bottom_y] and (not included[pt[0]][pt[1]]):
                diff = deltaE(pt, (pt_bottom_x, pt_bottom_y))
                if diff <= thresh:
                    included[pt[0]][pt[1]] = 1
            if not visited[pt_bottom_x][pt_bottom_y]:
                queue.append((pt_bottom_x, pt_bottom_y))
                visited[pt_bottom_x][pt_bottom_y] = 1

        pt_bottomleft_x, pt_bottomleft_y = pt[0] - 1, pt[1] - 1
        if not corner_pt((pt_bottomleft_x, pt_bottomleft_y)):
            if included[pt_bottomleft_x][pt_bottomleft_y] and (not included[pt[0]][pt[1]]):
                diff = deltaE(pt, (pt_bottomleft_x, pt_bottomleft_y))
                if diff <= thresh:
                    included[pt[0]][pt[1]] = 1
            if not visited[pt_bottomleft_x][pt_bottomleft_y]:
                queue.append((pt_bottomleft_x, pt_bottomleft_y))
                visited[pt_bottomleft_x][pt_bottomleft_y] = 1

    print (' -- Iters : ',iters, '||  Visited : ', np.unique(visited, return_counts = True), ' || Inlcluded : ', np.unique(included, return_counts = True))

    return 1

def flood_fill_improve():
    pass

if __name__ == "__main__":    
    ## PARAMS
    DIR = '/home/strider/Playment/code/segmentation_tools/githubrepos/images_floodfill'
    # filename = os.path.join(DIR, 'Zisserman_FaceMatching_small.png')
    # filename = os.path.join(DIR, 'Sky_Day_Cloudy_Large_Cropped.png')
    # filename = os.path.join(DIR, 'Sky_Day_Cloudy_Large.png'); point_start = (100, 700); thresh = 3
    # filename = os.path.join(DIR, 'Sky_Day_Cloudy_Large.png'); point_start = (350, 800); thresh = 5
    filename = os.path.join(DIR, 'Sky_Day_Cloudy_Large.png'); point_start = (300, 375); thresh = 5
    s = 5

    ## IMG CONVERSION
    img_rgb = io.imread(filename)
    img_lab = color.rgb2lab(img_rgb/255.0)  #  rgb2lab assumes that the RGB is standardized to range between 0 and 1
    plotMinMax(img_lab,labels=["L","a","b"])    
    h, w, d = img_lab.shape
    print (' --> Shape : ', img_lab.shape)
    print (' --> Total iters : ', h *w)

    ## FLOOD FILL ALGO
    visited  = np.zeros((h, w))
    included = np.full((h, w), 0)
    flood_fill3(point_start)
    flood_fill_improve()
    
    print (' - Final Output : ', included)

    ## PLOTTING
    if 0:
        f, axarr = plt.subplots(2,3, figsize=(15,15))
        axarr[0][0].imshow(img_rgb)
        axarr[0][0].scatter(point_start[1], point_start[0], s = s)
        axarr[0][0].set_title('RGB Space')
        axarr[0][1].imshow(img_lab)
        axarr[0][1].scatter(point_start[1], point_start[0], s = s)
        axarr[0][1].set_title('Lab Space')
        axarr[0][2].imshow(img_lab, cmap='gray')
        axarr[0][2].scatter(point_start[1], point_start[0], s = s)
        axarr[0][2].set_title('Lab Space - Gray')

        axarr[1][0].set_title('Initial Mask')
        axarr[1][0].imshow(np.full((h, w), 0.5), cmap='gray')
        axarr[1][0].scatter(point_start[1], point_start[0], s = s)
        axarr[1][1].set_title('Final Mask (see white)')
        axarr[1][1].imshow(included, cmap='gray')
        axarr[1][1].scatter(point_start[1], point_start[0], s = s)
        axarr[1][2].imshow(img_rgb)
        axarr[1][2].imshow(included, cmap='gray', alpha=0.6)
        axarr[1][2].scatter(point_start[1], point_start[0], s = s)
        
    else:
        f, axarr = plt.subplots(1)
        axarr.imshow(img_rgb)
        axarr.imshow(included, cmap='gray', alpha=0.6)
        axarr.scatter(point_start[1], point_start[0], s = s)

    plt.show()