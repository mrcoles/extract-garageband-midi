
Extract MIDI from a GarageBand track
====================================

You can find info [here](http://scotttroyer.com/2014/05/export-midi-from-garageband/) on how to extract a MIDI (.mid) file from a GarageBand track.

It references a downloadable Apple droplet app built by Lars Kobbe called [GB2MIDI](http://www.larskobbe.de/midi-export-in-apples-garageband/) that does the final step.

He helpfully mentioned that the MIDI file is inside GarageBand .aif loop files between the values of “MTrk” and “CHS” inside the file. So, as an alternative, I wrote a python script that also extract the MIDI file.

## Examples

List the loops that you have created:

```bash
$ python3 extract_midi.py --list

## Found 1 loop file:

  '/Users/pcoles/Library/Audio/Apple Loops/User Loops/SingleFiles/test - loop.aif'

Copy-paste the path to any of those files to this command, to extract a .mid file.
```

Export the loop:

```bash
$ python3 extract_midi '/Users/pcoles/Library/Audio/Apple Loops/User Loops/SingleFiles/test - loop.aif'
```

For more info, run the script with `--help`.


## Test it out

It seems like Mac OS X no longer has default support for directly playing MIDI files? This nifty shell command will save your day!

```
brew install timidity
timidity your_file.mid
```
