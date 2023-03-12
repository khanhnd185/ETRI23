import os
from tqdm import tqdm
import argparse

if __name__ == '__main__':

    """Parameters"""
    parser = argparse.ArgumentParser(description="Generate dataset file")
    parser.add_argument("--datadir", help='Data directory', default='../../../Data/KEMD/KEMDy20_v1_1/')
    parser.add_argument("--outdata", help='Output data file name', default='train_data.tsv')
    parser.add_argument("--outlabel", help='Output laebl file name', default='train_labels.csv')

    args = parser.parse_args()

    label_dir = args.datadir + 'annotation/'
    input_dir = args.datadir + 'wav'


    label_files = os.listdir(label_dir)
    print(len(label_files))

    conversations = []

    for file in label_files:
        label_path = label_dir + file
        with open(label_path, 'r') as f:
            lines = f.readlines()[2:]

        utterances = []
        prev_script = '01'

        for line in lines:
            segment, _, _, _, label = line.strip().split(',')[3:8]

            session =  segment[4:6]
            script = segment[13:15]
            user = segment[20:24]
            scene = segment[:15]

            if prev_script != script:
                conversations.append(utterances)
                prev_script = script
                utterances = []


            transcript_file = "{}/Session{}/{}.txt".format(input_dir, session, segment)
            with open(transcript_file, 'r', errors='ignore') as f:
                utterance = f.readlines()[0].strip()

            utterances.append({'id': segment, 'person': user, 'sentence': utterance, 'scene': scene, 'emotion': label})

        conversations.append(utterances)

    with open(args.outdata, 'w') as f:
        f.write('sentence_id\tperson\tsentence\tscene\n')
        for conversation in conversations:
            for utterance in conversation:
                line = "{}\t{}\t{}\t{}\n".format(utterance['id'], utterance['person'], utterance['sentence'], utterance['scene'])
                f.write(line)

    with open(args.outlabel, 'w') as f:
        f.write('sentence_id,label\n')
        for conversation in conversations:
            for utterance in conversation:
                line = "{},{}\n".format(utterance['id'], utterance['emotion'])
                f.write(line)

