#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
// Include that allows to print result as an image
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"

// Default size of image
#define X 1280
#define Y 720
#define MAX_ITER 10000

// function calc_mandelbrot(image):
//     for each (X,Y) do:
//         x = 0.0
//         y = 0.0
//         cx = mapped x_pixel_idx to Mandelbrot x-axis [-2.5, 1]
//         cy = mapped y_pixel_idx to Mandelbrot y-axis [-1, 1]
//         iteration = 0
//         while (x*x + y*y <= 2*2 AND iteration < MAX_ITER) do:
//             x_tmp = x*x - y*y + cx
//             y = 2*x*y + cy
//             x = x_tmp
//             iteration = iteration + 1

//         norm_iteration = mapped iteration to pixel range [0, 255]
//         image[y_pixel][x_pixel] = norm_iteration

void calc_mandelbrot(uint8_t image[Y][X]) {
	// check out the no. of array rows
	for (int py =  0; py < Y; py++){
		for (int px = 0; px < X; px++){

			double x = 0.0, y = 0.0;
			double cx = (double)px / X * 3.5 - 2.5;
			double cy = (double)py / Y * 2.0 - 1.0;
			int iteration = 0;
			while (x*x + y*y <= 2*2 && iteration< MAX_ITER){
				double x_tmp = x*x - y*y + cx;
				y = 2*x*y + cy;
				x = x_tmp;
				iteration++;
			}

			int norm_iteration = iteration * 255 / MAX_ITER;
			image[py][px] = (uint8_t)norm_iteration;
		}
	}
}

int main() {
	
	uint8_t image[Y][X];

	struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

	calc_mandelbrot(image);
	clock_gettime(CLOCK_MONOTONIC, &end);
	double elapsed = (end.tv_sec  - start.tv_sec) +
                     (end.tv_nsec - start.tv_nsec) / 1e9;


	printf("time: %2.4f seconds\n", elapsed);

	const int channel_nr = 1, stride_bytes = 0;
	stbi_write_png("mandelbrot.png", X, Y, channel_nr, image, stride_bytes);
	return EXIT_SUCCESS;
}