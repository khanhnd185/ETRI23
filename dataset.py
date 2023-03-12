from torch.utils.data import Dataset

class KEMD20_Text(Dataset):
    def __init__(self, tokenizer, data_file_name, label_file_name=None):
        super(KEMD20_Text, self).__init__()
        with open(data_file_name, 'r', encoding='utf-8', errors='ignore') as f:
            data_file = f.readlines()[1:]
        if label_file_name:
            with open(label_file_name, 'r', encoding='utf-8') as f:
                label_file = f.readlines()[1:]

        self.dialogs = [] 
        self.labelList = sorted({"angry", "sad", "happy", "disgust", "fear", "surprise", "neutral"})

        skip_list = []
        token_list = []
        return_list = []
        speaker_list = []
        speaker_name_list = []

        pre_scene = ""

        for i, data in enumerate(data_file):
            sentence_id, person, sentence, scene = data.strip().split('\t')
            if label_file_name:
                sentence_id, label = label_file[i].strip().split(',')
            
            if pre_scene != scene and len(token_list) > 0:
                self.dialogs.append((
                    token_list,
                    speaker_list,
                    skip_list,
                    return_list
                ))

                skip_list = []
                token_list = []
                return_list = []
                speaker_list = []
                speaker_name_list = []

                pre_scene = scene

            if person not in speaker_name_list:
                speaker_name_list.append(person)

            speaker_id = speaker_name_list.index(person)
            token = tokenizer.tokenize(sentence)
            token = tokenizer.convert_tokens_to_ids(token)
            skip_list.append(False)
            token_list.append(token)
            speaker_list.append(speaker_id)

            if label_file_name:
                return_list.append(self.labelList.index(label))
            else:
                return_list.append(int(sentence_id))


        if len(token_list) > 0:
            self.dialogs.append((
                token_list,
                speaker_list,
                skip_list,
                return_list
            ))



    def __len__(self):
        return len(self.dialogs)

    def __getitem__(self, idx):
        return self.dialogs[idx]

 