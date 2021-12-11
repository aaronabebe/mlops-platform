from clearml import StorageManager, Dataset
import argparse


def main():
	args = get_parser().parse_args()

	if args.path.startswith('http'):
			manager = StorageManager()
			
			dataset_path = manager.get_local_copy(
				remote_url=args.path
			)
	else:
		dataset_path = args.path

	dataset = Dataset.create(
		dataset_name=args.name, dataset_project=args.project
	)

	dataset.add_files(path=dataset_path)
	
	dataset.upload()
	dataset.finalize()


def get_parser():
	parser = argparse.ArgumentParser(description='clearML dataloader helper')
	parser.add_argument('--path', required=True, 
						help='local directory or remote link to upload as dataset')
	parser.add_argument('--name', required=True, 
						help='name of the dataset')
	parser.add_argument('--project', required=False, default='data_management', 
						help='name of the clearML project')
	return parser


if __name__=='__main__':
	main()
