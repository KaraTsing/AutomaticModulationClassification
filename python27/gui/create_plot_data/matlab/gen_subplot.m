function gen_subplot(vec_file,titlestr, subpl1, subpl2, subpl3)
% read a file and plot it
%
%
filelen = 2048;
vec = read_complex_binary(vec_file, filelen);

subplot(subpl1, subpl2, subpl3);
hold on;
title(titlestr, 'FontSize', 20)

skip = randi([800, 1600]);
len = 128;

plot(1:len, real(vec(skip:skip+len-1)),'LineWidth',2,...
    'Color','b',...
    'MarkerSize',10);
xlim([-5, 132]);
set(gca,'XColor','none')
set(gca,'YColor','none')
set(gca,'xtick',[]);
set(gca,'ytick',[]);
set(gca,'yticklabel',[]);
set(gca,'xticklabel',[]);
plot( 1:len, imag(vec(skip:skip+len-1)), 'LineWidth',2,...
    'Color','r',...
    'MarkerSize',10);
xlim([-5, 132]);
set(gca,'XColor','none')
set(gca,'YColor','none')
set(gca,'xtick',[]);
set(gca,'xticklabel',[]);
set(gca,'ytick',[]);
set(gca,'yticklabel',[]);
hold off;