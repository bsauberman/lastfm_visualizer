import cv2
import glob

frameSize = (4000,3000)
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, frameSize)
count = 0

for filename in sorted(glob.glob('images/*.png')):
    img = cv2.imread(filename)
    out.write(img)
    print(filename)
    count = count + 1
    #if count > 20: break

out.release()
print('released')