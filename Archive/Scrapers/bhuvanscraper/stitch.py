import glob
import numpy as np
import PIL
from PIL import Image
PIL.Image.MAX_IMAGE_PIXELS = 933120000

extension = 'png'
        #os.chdir(path)

for year in ['2021']:
    result = glob.glob(year+'_*.{}'.format(extension))
    k = np.empty(shape=(24320, 36864), dtype='uint8')
    for file in result:
        print(file)
        img = Image.open(file)
        image1_ar = np.asarray(img).copy()
        if image1_ar.shape[1] != 36864:
            print('Issue')
            image1_ar = np.lib.pad(image1_ar, ((0, 0), (0, 36864 - image1_ar.shape[1])), 'constant',
                                   constant_values=(255))
        else:
            pass
        image1_ar[:, :][(image1_ar[:, :] == 255)] = 0
        image1_ar[:, :][(image1_ar[:, :] == 179)] = 1
        k = np.add((image1_ar), k)

    #h = k.copy()
    #for i in unique_values:
     #   substitute = round((i / (len(unique_values) - 1) * 179))
      #  print("For pixel value {}, substitue is {}".format(i, substitute))
       # h[:, :][(h[:, :] == i)] = substitute
    image1 = Image.fromarray(k)
    image1.save(year+'_stitched.png')
    print('stitched')

