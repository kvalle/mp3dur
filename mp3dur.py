import sys
import eyeD3
import fnmatch
import os

def color(text, color):
    cmap = {'red': '0;31', 'bright':'1;39'}
    return "\33["+cmap[color]+"m"+text+"\33[0m"

def get_play_time(path):
    if eyeD3.isMp3File(path):
        audioFile = eyeD3.Mp3AudioFile(path)
        tag = audioFile.getTag()
        return audioFile.getPlayTime()
    else:
        return 0

def list_files(root_path='.', pattern='*', recursive=False, verbose=False):
    def _add_dir():
        tot = 0
        matches = fnmatch.filter(files, pattern)
        if verbose: print '  '+root,
        for filename in matches:
            path = os.path.join(root, filename)
            if os.path.isfile(path):
                tot += get_play_time(path)
        if verbose: print ' ('+str(len(matches))+' files, '+format_time(tot)+')'
        return tot
    time = 0
    if verbose: print 'Searching folders:'
    if recursive:
        for root, dirs, files in os.walk(root_path):
            time += _add_dir()
    else:
        files = os.listdir(root_path)
        root = root_path
        time += _add_dir()
    return time

def format_time(secs):
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
        err_opts = list(set(options) - set(['-r', '--recursive', '-v', '--verbose']))
        for opt in err_opts:
            print color('!! option "'+opt+'" not recognized.','red')
        if err_opts:
            exit(1)
    except:
        print
        print "ABOUT:"
        print color("  Script for listing durations of all MP3 files in a folder.", 'bright')
        print
        print "USAGE:"
        print color("  python mp3dur.py path [-OPTION]", 'bright')
        print
        print "OPTIONS:"
        print color("  -r, --recursive", 'bright')
        print "             search subfolders recursively"
        print
        print color("  -v, --verbose", 'bright')
        print "             print name of searched folders"
        print
        exit(0)
    if os.path.isdir(path):
        secs = list_files(path, '*.mp3', recursive=rec, verbose=verb)
        print 'Total playtime:'
        print color('  '+format_time(secs), 'bright')
    else:
        print color('!! directory "'+path+'" not found.', 'red')
        exit(1)
