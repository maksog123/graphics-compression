import xml.etree.ElementTree as ET
from shapely.geometry import Point, MultiPolygon
from shapely.ops import unary_union
import re
import time
import os
import numpy as np
import matplotlib.pyplot as plt

def add_path_to_svg(svg_file, output_file, path_data, path_attributes=None):
    tree = ET.parse(svg_file)
    root = tree.getroot()
    ns = {'svg': 'http://www.w3.org/2000/svg'}
    ET.register_namespace('', ns['svg'])
    
    svg_tag = root if root.tag.endswith('svg') else root.find('.//svg:svg', ns)
    
    path_element = ET.Element('path', {'d': path_data})
    if path_attributes:
        for key, value in path_attributes.items():
            path_element.set(key, value)
    
    svg_tag.append(path_element)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)
    print(f"Saved merged SVG file: {output_file}")

def extract_circle_radius_from_svg(pliksvg):
    tree = ET.parse(pliksvg)
    root = tree.getroot()
    namespace = {'svg': root.tag.split('}')[0].strip('{')} if '}' in root.tag else {}
    
    for path in root.findall(".//svg:path", namespaces=namespace):
        path_data = path.get("d")
        if path_data and is_circle_path(path_data):
            return extract_radius_from_path_data(path_data)
    return None

def is_circle_path(path_data):
    return "C" in path_data and path_data.strip().endswith("z")

def extract_radius_from_path_data(path_data):
    match = re.match(r"M\s[\d.-]+\s([\d.-]+)", path_data)
    return float(match.group(1)) if match else None

def plot_to_paths(plot_svg):
    tree = ET.parse(plot_svg)
    root = tree.getroot()
    namespace = {'svg': 'http://www.w3.org/2000/svg', 'xlink': 'http://www.w3.org/1999/xlink'}
    
    for path in root.findall(".//svg:defs/svg:path", namespaces=namespace):
        circle_path_id = path.get("id")
        circle_path_data = path.get("d")
        break
    else:
        print("No circle path found in <defs>")
        return []
    
    circles = []
    styles_dic = {}

    path_ref = f"#{circle_path_id}"
    for use in root.findall(".//svg:use", namespaces=namespace):
        if use.get(f"{{{namespace['xlink']}}}href") == path_ref:
            if use.get("style") in  styles_dic:
                styles_dic[use.get("style")].append({
                    "center_x": use.get("x", "0"),
                    "center_y": use.get("y", "0"),
                    "path_data": circle_path_data,
                    "style": use.get("style")
                })
            else:
                styles_dic[use.get("style")] = [{
                    "center_x": use.get("x", "0"),
                    "center_y": use.get("y", "0"),
                    "path_data": circle_path_data,
                    "style": use.get("style")
                }]
    return styles_dic

def path_to_circle(list_of_paths, radius):
    out_circles = []
    for circle in list_of_paths:
        try:
            out_circles.append([float(circle["center_x"]), float(circle["center_y"]), float(radius)])
        except (ValueError, IndexError):
            print("Error parsing circle data, skipping circle.")
    return out_circles

def shapely_to_svg_path(geometry):
    if geometry.geom_type == 'Polygon':
        path = f"M {' '.join(f'{x},{y}' for x, y in geometry.exterior.coords)} Z"
        for interior in geometry.interiors:
            path += f" M {' '.join(f'{x},{y}' for x, y in interior.coords)} Z"
        return path
    elif geometry.geom_type == 'MultiPolygon':
        paths = []
        for poly in geometry.geoms:
            paths.append(f"M {' '.join(f'{x},{y}' for x, y in poly.exterior.coords)} Z")
            for interior in poly.interiors:
                paths.append(f"M {' '.join(f'{x},{y}' for x, y in interior.coords)} Z")
        return " ".join(paths)

def final_graph(pliksvg, clearsvg, point_framing=True):
    if point_framing:
        radius = extract_circle_radius_from_svg(pliksvg) + 0.5
    else:
        radius = extract_circle_radius_from_svg(pliksvg)
    
    circles1 = plot_to_paths(pliksvg)
    print(len(circles1))
    for style, circle in circles1.items():
        circles2 = path_to_circle(circle, radius)
        if circles2:
            print(f"{style}")
            shapes = [Point(x, y).buffer(radius) for x, y, r in circles2]
            new_union = unary_union(shapes)
        
        svg_path_data = shapely_to_svg_path(new_union)
        add_path_to_svg(clearsvg, pliksvg[:-4] + "_compressed.svg", svg_path_data, path_attributes={"style": style})

def extract_num_points(filename):
    """Extracts and prints the number of points from a filename in the format 'noisy_sin_{number of points}.svg'."""
    match = re.search(r'noisy_gauss(\d+)\.svg', filename)
    if match:
        num_points = int(match.group(1))
        return num_points

def extract_num_directory(directory):
    """Extracts and prints the number of points from a directory in the format 'noisy_sin_{number of points}'."""
    match = re.search(r'noisy_gaussian_(\d+)', directory)
    if match:
        num_dir = int(match.group(1))
        return num_dir

if __name__ == "__main__":
    # Ask about input files
    directories = [d for d in os.listdir() if d.startswith("noisy_gaussian")]
    print("Directories found:", directories)
    
    n = np.array([])
    times = np.array([])
    
    for directory in directories:
        files = [f for f in os.listdir(directory) if f.startswith("noisy") and not f.endswith("compressed.svg")]
        clearsvg = [f for f in os.listdir(directory) if f.startswith("clear")][0]
        print(f"\nDirectory: {directory}")
        print(f"\nFiles: {files}")
        #Example: Process each file
        for file in files:
            print(f"\nProcessing: {file}")
            n = np.append(n, extract_num_points(file))
            pliksvg = directory + "/" + file
            start_time = time.time()
            final_graph(pliksvg, clearsvg)
            execution_time = time.time() - start_time
            times = np.append(times, execution_time)
            print(f"Execution time: {execution_time} seconds")
        print(f"\nsizes: {n}")
        print(f"\ntimes: {times}")

        np.savetxt("time_complexity_data_" + str(extract_num_directory(directory)) + ".txt", np.column_stack((n, times)), fmt=["%d", "%e"], delimiter=",", header="n, time")
        print(f"\nSaved data to file time_complexity_data_{extract_num_directory(directory)}.txt")

        # plt.scatter(n, times, label='Data measured using our program', color='b', alpha=1, s=10)
        # plt.xlabel('Number of points')
        # plt.ylabel('Execution time (s)')
        # plt.title('Execution time vs. Number of points')
        # plt.savefig('time_complexity_vs_points.pdf', format='pdf')
        # plt.close()

        # plt.loglog(n, times, label='Data measured using our program', color='b', alpha=1, marker='o', linestyle='None')
        # plt.xlabel('Number of points')
        # plt.ylabel('Execution time (s)')
        # plt.title('Execution time vs. Number of points (log-log)')
        # plt.savefig('time_complexity_vs_points_loglog.pdf', format='pdf')
        # plt.close()