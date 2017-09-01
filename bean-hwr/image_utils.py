import numpy as np
from cnn.neural_net import NeuralNetwork
import os
from PIL import Image

path = os.path.dirname(__file__)

def encode_image(im):
    # 获取base64压缩前的图像
    im = im.convert('L')
    im_list = crop_image(im)
    array_list = []
    for im in im_list:
        im = pad_image(im)
        array_list.append(analyze_image(im))

    return array_list


def crop_image(image):
    def surrounds_8(point):
        result = []
        for x in range(point[0] - 1, point[0] + 2):
            for y in range(point[1] - 1, point[1] + 2):
                if ((x, y) is not point) and (x,y) in point_list and (x,y) not in record_list:
                    result.append((x,y))
        return result

    '''

    :param image:
    :return:
    '''
    im_array = image.load()
    width, height = image.size
    point_list = []  #所有非空白点
    image_list = []  #所有团的集合

    for i in range(width):
        for j in range(height):
            if im_array[i,j] != 255:
                point_list.append((i, j))

    while len(point_list):
        bfs_list = []  #记录bfs过程中的标记节点
        record_list = []  #记录团中所有节点
        ##记录新的连通图像
        new_image = Image.new("L", (width, height), 255)
        xmin = width - 1
        xmax = 0
        ymin = height - 1
        ymax = 0

        bfs_list.append(point_list.pop(0))
        record_list = bfs_list.copy()
        #bfs
        while len(bfs_list):
            temp_point = bfs_list.pop(0)
            x, y = temp_point
            new_image.putpixel((x,y),im_array[x,y])
            xmin = x if x < xmin else xmin
            xmax = x if x > xmax else xmax
            ymin = y if y < ymin else ymin
            ymax = y if y > ymax else ymax

            if temp_point in point_list:
                point_list.remove(temp_point)
            sur_points = surrounds_8(temp_point)
            bfs_list.extend(sur_points)
            record_list.extend(sur_points)

        image_list.append(new_image.crop((xmin,ymin,xmax,ymax)))

    return image_list

def pad_image(im):
    offset = 20
    im_array = np.asarray(im).astype(float)
    height = im_array.shape[0]
    width = im_array.shape[1]

    if width < height:
        diff = int((height - width)/2)
        im_array = np.lib.pad(im_array, ((offset,offset),(diff + offset,diff + offset)),'constant',constant_values=(255, 255))

    else:
        diff = int((width - height)/2)
        im_array = np.lib.pad(im_array, ((diff + offset, diff + offset), (offset, offset)), 'constant', constant_values=(255, 255))

    image = Image.fromarray(np.uint8(im_array))
    return image


def analyze_image(im):
    im = im.resize((28, 28))
    im_array = np.asarray(im).astype(np.float32)
    im_array = np.reshape(im_array, [1, 784])
    im_array.flags.writeable = True
    for i in range(784):
        im_array[0, i] = 1 - float((im_array[0, i]) / 255)

    im_array = np.reshape(im_array, [-1, 1, 28, 28])
    '''data pre-treatment'''
    W_conv1 = np.load(path + "/np_weights/W_conv1.npy")
    W_conv1 = np.reshape(W_conv1, [25, 6])

    W_conv2 = np.load(path + "/np_weights/W_conv2.npy")
    W_conv2 = W_conv2.transpose(2, 0, 1, 3)
    W_conv2 = np.reshape(W_conv2, [150, 16])

    W_conv3 = np.load(path + "/np_weights/W_conv3.npy")
    W_conv3 = W_conv3.transpose(2, 0, 1, 3)
    W_conv3 = np.reshape(W_conv3, [16 * 4 * 4, 120])

    cnn = NeuralNetwork(im_array.shape[1:],
                        [
                            {'type': 'conv', 'k': 6, 'u_type': 'adam', 'f': 5, 's': 1, 'p': 0},
                            {'type': 'pool'},
                            {'type': 'conv', 'k': 16, 'u_type': 'adam', 'f': 5, 's': 1, 'p': 0},
                            {'type': 'pool'},
                            {'type': 'conv', 'k': 120, 'u_type': 'adam', 'f': 4, 's': 1, 'p': 0},
                        ])

    cnn.layers[0].set_weights(W_conv1)
    cnn.layers[2].set_weights(W_conv2)
    cnn.layers[4].set_weights(W_conv3)

    cnn.epoch_count = 0

    result = cnn.output(im_array)
    #str = result.dumps()
    return result
