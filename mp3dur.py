import sys
import eyeD3
import fnmatch
import os

def get_play_time(path):
    if eyeD3.isMp3File(path):
        audioFile = eyeD3.Mp3AudioFile(path)
        tag = audioFile.getTag()
        return audioFile.getPlayTime()
    else:
        return 0

def list_files(root_path='.', pattern='*', recursive=False, verbose=False):
    def _add_dir():
        matches = fnmatch.filter(files, pattern)
        if verbose: print '  '+root+' ('+str(len(matches))+' files)'
        for filename in matches:
            path = os.path.join(root, filename)
            if os.path.isfile(path): fs.append(path)
    fs = []
    if verbose: print 'Searching folders:'
    if recursive:
        for root, dirs, files in os.walk(root_path):
            _add_dir()
    else:
        files = os.listdir(root_path)
        root = root_path
        _add_dir()
    return fs

def read_file_durations(files):
    seconds = 0
    for f in files:
        seconds += get_play_time(f)
    return seconds

def format_seconds(secs):
    hours = secs/3600
    mins = (secs-hours*3600)/60
    secs = secs%60
    return str(hours)+'h'+str(mins)+'m'+str(secs)+'s'

if __name__ == "__main__":
    rec = False
    verb = False
    try:
        path = sys.argv[1]
        options = sys.argv[2:]
        rec = '-r' in options or '-recursive' in options
        verb = '-v' in options or '-verbose' in options
        for opt in list(set(options) - set(['-r', '-recursive', '-v', '-verbose'])):
            print '!! Option "'+opt+'" not recognized.'
    except:
        print
        print "About:"
        print "  Script for listing durations of all MP3 files in a folder."
        print
        print "Usage:"
        print "  python mp3dur.py path [-OPTION]"
        print
        print "OPTIONS:"
        print "  -r(ecursive)   recursively for subfolders"
        print "  -v(erbose)     print searched folders"
        print
        exit(0)
    if os.path.isdir(path):
        files = list_files(path, '*.mp3', recursive=rec, verbose=verb)
        secs = read_file_durations(files)
        print 'Total playtime:'
        print '  '+format_seconds(secs)
    else:
        print '!! provided directory "'+path+'" not found.'
