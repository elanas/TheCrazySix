from collections import namedtuple

class HighscoreManager:
    NUM_HIGHSCORES = 4
    DEFAULT_FILE_PATH = 'highscores.txt'
    PARSE_ERROR = 'The highscore file is formatted incorrectly.'
    PAIR_SEPARATOR = '^&~`-'  # this seems random enough?
    HighscoreEntry = namedtuple('HighscoreEntry', 'name score')
    EMPTY_ENTRY = HighscoreEntry('-----', '-----')
    highscore_list = None

    def __init__(self, file_path=DEFAULT_FILE_PATH):
        self.file_path = file_path
        self.load()

    def load(self):
        self.highscore_list = list()
        try:
            with open(self.file_path, 'r') as file_handle:
                for line in [l.strip() for l in file_handle]:
                    if len(line) == 0:
                        continue
                    parts = line.split(HighscoreManager.PAIR_SEPARATOR)
                    try:
                        new_highscore = HighscoreManager.HighscoreEntry(
                            name=parts[0], score=int(float(parts[1])))
                    except Exception:
                        raise Exception(HighscoreManager.PARSE_ERROR)
                    self.highscore_list.append(new_highscore)
        except IOError:
            self.highscore_list = list()

    def add(self, name, score):
        new_highscore = HighscoreManager.HighscoreEntry(name=name, score=score)
        if self.highscore_list is None:
            self.highscore_list = list(new_highscore)
        else:
            pos = -1
            for i in range(0, len(self.highscore_list)):
                if self.highscore_list[i].score < score:
                    pos = i
                    break
            if pos == -1:
                pos = len(self.highscore_list)
            self.highscore_list.insert(pos, new_highscore)
        self.save()

    def save(self):
        with open(self.file_path, 'w') as file_handle:
            curr_num = 0
            for highscore in self.highscore_list:
                if curr_num >= HighscoreManager.NUM_HIGHSCORES:
                    break
                file_handle.write(highscore.name)
                file_handle.write(HighscoreManager.PAIR_SEPARATOR)
                file_handle.write(str(highscore.score))
                file_handle.write('\n')
                curr_num += 1

    def get_list(self):
        if len(self.highscore_list) == HighscoreManager.NUM_HIGHSCORES:
            return self.highscore_list
        temp_list = list(self.highscore_list)
        if len(temp_list) < HighscoreManager.NUM_HIGHSCORES:
            for i in range(0, HighscoreManager.NUM_HIGHSCORES -
                           len(self.highscore_list)):
                temp_list.append(HighscoreManager.EMPTY_ENTRY)
        else:
            temp_list = temp_list[0:HighscoreManager.NUM_HIGHSCORES]
        return temp_list
