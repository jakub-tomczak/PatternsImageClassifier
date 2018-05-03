$env:IMAGE_SIZE=224
$env:ARCHITECTURE="mobilenet_0.50_$env:IMAGE_SIZE"
python ..\\tensorflow\\retrain.py --bottleneck_dir=..\\output\\bottlenecks --how_many_training_steps=1000 --model_dir=..\\tensorflow\\models\\ --summaries_dir=..\\output\\pattern_training_summaries\\"$env:ARCHITECTURE"  --output_graph=..\\output\\retrained_graph_patterns.pb  --output_labels=..\\output\\retrained_labels.txt  --architecture="$env:ARCHITECTURE" --image_dir=..\\patterns
