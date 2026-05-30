from backend.utils.taiwan_map import COUNTY_BOX

def crop_region(img, region):

    x1, x2, y1, y2 = COUNTY_BOX[region]

    return img[y1:y2, x1:x2]