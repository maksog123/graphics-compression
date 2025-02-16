# graphics-compression
This repository provides tools for compressing vector graphics, specifically designed for scientific applications using Python. The approach reduces data while preserving the visual integrity of the graphics.

Folder Structure

time_complexity_analysis

This folder contains scripts for analyzing the time complexity of graph compression:

plots_time_complexity.py – Generates plots for experimental data analysis.

graphs_compression_time.py – Compresses each graph, measures compression time based on the number of points, and saves the results in a text file.

time_complexity_fits.py – Performs and visualizes linear fits to the experimental data.

programs_to_use

This folder contains two scripts for compressing graphs:

graphs_compression_file.py – Compresses a single SVG plot with data points, using a background-only version (frame, labels, etc.) as a reference.

graphs_compression_directory.py – Compresses all SVG files in a directory that share the same background, using a reference SVG file without data points.
