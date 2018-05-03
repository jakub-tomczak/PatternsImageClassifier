param([string]$filename)
echo "Trying to classify an image $filename"
python ..\\tensorflow\\label_image.py --graph=..\\output\\retrained_graph_patterns.pb --labels=..\\output\\retrained_labels.txt --image=..\\resources\\decor\\$filename