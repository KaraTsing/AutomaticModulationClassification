%% fig crop

% RECT is a 4-element vector with the form [XMIN YMIN WIDTH HEIGHT];
xmin = 217;
ymin = 106;
xmax = 1671;
ymax = 1003;
crop_rect =  [xmin, ymin, xmax-xmin, ymax-ymin]; 

im20 = imread('20dB.png');
im20c = imcrop(im20, crop_rect);
imwrite(im20c, 'im20c.png', 'PNG');

im0 = imread('0dB.png');
im0c = imcrop(im0, crop_rect);
imwrite(im0c, 'im0c.png', 'PNG');

imm20 = imread('-20dB.png');
imm20c = imcrop(imm20, crop_rect);
imwrite(imm20c, 'imm20c.png', 'PNG');

% whitebg(figure);
% imshow(im20c);
