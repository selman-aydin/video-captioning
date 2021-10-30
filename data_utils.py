from torch import load, LongTensor
from torch.utils.data import Dataset, DataLoader
from text_processing import get_vocab

PARAMS = {'batch_size': 64,
            'shuffle': True,
            'num_workers': 6}

class TestDataset(Dataset):
    'Characterizes a dataset for PyTorch'
    def __init__(self, paths, visual_feature_folder, audial_feature_folder):
        'Initialization'
        self.paths = paths
        self.audial_feature_folder = audial_feature_folder
        self.visual_feature_folder = visual_feature_folder

    def __len__(self):
        'Denotes the total number of samples'
        return len(self.paths)

    def __getitem__(self, index):
        'Generates one sample of data'
        # Select sample

        name = self.paths[index] + ".pt"
        visual_feature = load(self.visual_feature_folder / name, map_location='cpu')
        audial_feature = load(self.audial_feature_folder / name, map_location='cpu')
        id = int(self.paths[index][5:])

        return visual_feature, audial_feature, id

class TrainDataset(Dataset):
    'Characterizes a dataset for PyTorch'
    def __init__(self, ids, captions, visual_feature_folder, audial_feature_folder):
        'Initialization'
        self.ids = ids
        self.captions = captions
        self.visual_feature_folder = visual_feature_folder
        self.audial_feature_folder = audial_feature_folder

    def __len__(self):
        'Denotes the total number of samples'
        return len(self.ids)

    def __getitem__(self, index):
        'Generates one sample of data'
        # Select sample

        name = self.ids[index] + ".pt"
        visual_feature = load(self.visual_feature_folder / name, map_location='cpu')
        audial_feature = load(self.audial_feature_folder / name, map_location='cpu')
        
        tokens = self.captions[index]
        tokens = LongTensor(tokens)

        return visual_feature, audial_feature, tokens


def get_loader_and_vocab(dt):
    train_data, val_ids, test_ids = dt.load_data()
    processed_paths, processed_captions, vocab, tokenizer = get_vocab(train_data)
    train_dataset = TrainDataset(ids=processed_paths, captions=processed_captions, visual_feature_folder=dt.train_visual_features_folder, audial_feature_folder=dt.train_audial_features_folder)
    train_loader = DataLoader(train_dataset, **PARAMS)
    val_dataset = TestDataset(paths=val_ids, visual_feature_folder=dt.train_visual_features_folder, audial_feature_folder=dt.train_audial_features_folder)
    val_loader = DataLoader(val_dataset, **PARAMS)
    test_dataset = TestDataset(paths=test_ids, visual_feature_folder=dt.test_visual_features_folder, audial_feature_folder=dt.test_audial_features_folder)
    test_loader = DataLoader(test_dataset, **PARAMS)

    return train_loader, val_loader, test_loader, vocab

