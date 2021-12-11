from clearml import StorageManager, Dataset


def main():
	manager = StorageManager()
	
	dataset_path = manager.get_local_copy(
		remote_url='https://data.deepai.org/mnist.zip'
	)

	dataset = Dataset.create(
		dataset_name='mnist_dataset', dataset_project='data_management'
	)

	dataset.add_files(path=dataset_path)
	
	dataset.upload()
	dataset.finalize()


if __name__=='__main__':
	main()
