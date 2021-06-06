from pyprojroot import here
from sklearn.metrics import roc_auc_score
from tqdm import tqdm, trange

from MIDAS import FilteringCore, NormalCore, RelationalCore

if __name__ == '__main__':
	prefix = here()  # Detect your project root
	pathData = prefix / 'data/DARPA/darpa_processed.csv'
	pathLabel = prefix / "data/DARPA/darpa_ground_truth.csv"
	pathScore = prefix / 'out/Score.txt'

	data = [[int(item) for item in line.split(b',')] for line in tqdm(pathData.read_bytes().splitlines(), 'Load Dataset', unit_scale=True)]
	label = list(map(int, pathLabel.read_bytes().splitlines()))
	midas = NormalCore(2, 1024)
	# midas = RelationalCore(2, 1024)
	# midas = FilteringCore(2, 1024, 1e3)
	score = [0.0] * len(label)
	for i in trange(len(label), desc=midas.nameAlg, unit_scale=True):
		score[i] = midas.Call(*data[i])
	print(f"ROC-AUC = {roc_auc_score(label, score):.4f}")
	print(f"# Raw scores will be exported to")  # Comment this line and below if you don't need to export
	print(f"# {prefix / 'out/Score.txt'}")
	pathScore.parent.mkdir(exist_ok=True)
	with pathScore.open('w', newline='\n') as file:
		for line in tqdm(score, 'Export Scores', unit_scale=True):
			file.write(f'{line}\n')
	pass
