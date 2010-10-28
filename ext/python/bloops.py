#!/bin/env python

from ctypes import *
from ctypes.util import find_library

BLOOPS_PATH = find_library("bloopsaphone")
if not BLOOPS_PATH:
    raise ImportError, "bloopsaphone not found"

lib = CDLL(BLOOPS_PATH)
if not lib:
    raise ImportError, "could not import bloopsaphone"

## bloopsaphone.h definitions

# enum bloopsstate
BLOOPS_STOP = 0
BLOOPS_PLAY = 1

# enum bloopsawaveform
BLOOPS_SQUARE = 0
BLOOPS_SAWTOOTH = 1
BLOOPS_SINE = 2
BLOOPS_NOISE = 3

# enum bloopsafxcmd
BLOOPS_FX_VOLUME = 0
BLOOPS_FX_PUNCH = 1
BLOOPS_FX_ATTACK = 2
BLOOPS_FX_SUSTAIN = 3
BLOOPS_FX_DECAY = 4
BLOOPS_FX_SWEEP = 5
BLOOPS_FX_SQUARE = 6
BLOOPS_FX_VIBE = 7
BLOOPS_FX_VSPEED = 8
BLOOPS_FX_VDELAY = 9
BLOOPS_FX_LPF = 10
BLOOPS_FX_LSWEEP = 11
BLOOPS_FX_RESONANCE = 12
BLOOPS_FX_HPF = 13
BLOOPS_FX_HSWEEP = 14
BLOOPS_FX_ARP = 15
BLOOPS_FX_ASPEED = 16
BLOOPS_FX_PHASE = 17
BLOOPS_FX_PSWEEP = 18
BLOOPS_FX_REPEAT = 19

# struct bloopsaparams
class c_bloopsaparams(Structure):pass
c_bloopsaparams._fields_ = [
        ('type', c_int), # actually it's a bloopswaveform (enum)
        ('pan', c_ubyte),
        ('volume', c_float),
        ('punch', c_float),
        ('attack', c_float),
        ('sustain', c_float),
        ('decay', c_float),
        # pitch
        ('freq', c_float),
        ('limit', c_float),
        ('slide', c_float),
        ('dslide', c_float),
        # square wave
        ('square', c_float),
        ('sweep', c_float),
        # vibrato
        ('vibe', c_float),
        ('vspeed', c_float),
        ('vdelay', c_float),
        # hi-pass, lo-pass
        ('lpf', c_float),
        ('lsweep', c_float),
        ('resonance', c_float),
        ('hpf', c_float),
        ('hsweep', c_float),
        # arpeggiator
        ('arp', c_float),
        ('aspeed', c_float),
        # phaser
        ('phase', c_float),
        ('psweep', c_float),
        ('repeat', c_float) 
    ]

# struct bloopsaphone
class c_bloopsaphone(Structure):pass
c_bloopsaphone._fields_ = [
        ('refcount', c_uint),
        ('params', c_bloopsaparams)
    ]

# struct bloopsafx_tag
class c_bloopsafx(Structure):pass
c_bloopsafx._fields_ = [
        ('cmd', c_int), # bloopsfxcmd
        ('val', c_float),
        ('mod', c_char),
        ('next', POINTER(c_bloopsafx))
    ]

# struct bloopsanote
class c_bloopsanote(Structure):pass
c_bloopsanote._fields_ = [
        ('tone', c_char),
        ('octave', c_char),
        ('duration', c_char),
        ('FX', POINTER(c_bloopsafx))
    ]

# struct bloopsatrack
class c_bloopsatrack(Structure):pass
c_bloopsatrack._field_ = [
        ('refcount', c_uint),
        ('nlen', c_int),
        ('capa', c_int),
        ('notes', POINTER(c_bloopsanote)),
        ('params', c_bloopsaparams)
    ]

# struct bloopsavoice
class c_bloopsavoice(Structure):pass
c_bloopsavoice._field_ = [
        ('bloopsatrack', POINTER(c_bloopsatrack)),
        ('params', c_bloopsaparams),
        ('frames', c_int),
        ('nextnote', c_int * 2), # 2 value int array
        ('volume', c_float),
        ('freq', c_float),
        ('state', c_int), # bloopsastate
        ('stage', c_int),
        ('time', c_int),
        ('length', c_int * 3),
        ('period', c_double),
        ('maxperiod', c_double),
        ('slide', c_double),
        ('dslide', c_double),
        ('square', c_float),
        ('sweep', c_float),
        ('phase', c_int),
        ('iphase', c_int),
        ('phasex', c_int),
        ('fphase', c_float),
        ('dphase', c_float),
        ('phaser', c_float * 1024),
        ('noise', c_float * 32),
        ('filter', c_float * 8),
        ('vibe', c_float),
        ('vspeed', c_float),
        ('vdelay', c_float),
        ('repeat', c_int),
        ('limit', c_int),
        ('arp', c_double),
        ('atime', c_int),
        ('alimit', c_int),
    ]

BLOOPS_MAX_TRACKS = 64
BLOOPS_MAX_CHANNELS = 64

class c_bloops(Structure):pass
c_bloops._fields_ = [
        ('refcount', c_uint),
        ('tempo', c_int),
        ('volume', c_float),
        ('voices', c_bloopsavoice * BLOOPS_MAX_TRACKS),
        ('state', c_int), # c_bloopsastate
    ]

class c_bloopsmix(Structure):pass
c_bloopsmix._fields_ = [
        ('B', POINTER(c_bloops) * BLOOPS_MAX_CHANNELS), # c_bloopsastate
        ('stream', c_void_p),
    ]

## prototypes

# bloops *bloops_new();
# void bloops_ref(bloops *);
# void bloops_destroy(bloops *);
lib.bloops_new.restype = POINTER(c_bloops)
lib.bloops_ref.argtypes = [POINTER(c_bloops)]
lib.bloops_destroy.argtypes = [POINTER(c_bloops)]

# void bloops_clear(bloops *);
# void bloops_tempo(bloops *, int tempo);
# void bloops_play(bloops *);
# void bloops_stop(bloops *);
# int bloops_is_done(bloops *);
lib.bloops_clear.argtypes = [POINTER(c_bloops)]
lib.bloops_tempo.argtypes = [POINTER(c_bloops), c_int]
lib.bloops_play.argtypes = [POINTER(c_bloops)]
lib.bloops_stop.argtypes = [POINTER(c_bloops)]
lib.bloops_is_done.argtypes = [POINTER(c_bloops)]

# bloopsatrack *bloops_track(bloops *, bloopsaphone *, char *, int);
# bloopsatrack *bloops_track2(bloops *, bloopsaphone *, char *);
# void bloops_track_ref(bloopsatrack *);
# void bloops_track_destroy(bloopsatrack *);
lib.bloops_track.restype = POINTER(c_bloopsatrack)
lib.bloops_track.argtypes = [POINTER(c_bloops), POINTER(c_bloopsaphone), c_char_p, c_int]
lib.bloops_track2.restype = POINTER(c_bloopsatrack)
lib.bloops_track2.argtypes = [POINTER(c_bloops), POINTER(c_bloopsaphone), c_char_p]
lib.bloops_track_ref.argtypes = [POINTER(c_bloopsatrack)]
lib.bloops_track_destroy.argtypes = [POINTER(c_bloopsatrack)]

# bloopsaphone *bloops_square();
# bloopsaphone *bloops_sound_file(bloops *, char *);
# void bloops_sound_copy(bloopsaphone *, bloopsaphone const *);
# void bloops_sound_ref(bloopsaphone *);
# void bloops_sound_destroy(bloopsaphone *);
lib.bloops_square.restype = POINTER(c_bloopsaphone)
lib.bloops_sound_file.restype = POINTER(c_bloopsaphone)
lib.bloops_sound_file.argtypes = [POINTER(c_bloopsaphone), c_char_p]
lib.bloops_sound_copy.argtypes = [POINTER(c_bloopsaphone), POINTER(c_bloopsaphone)]
lib.bloops_sound_ref.argtypes = [POINTER(c_bloopsaphone)]
lib.bloops_sound_destroy.argtypes = [POINTER(c_bloopsaphone)]

# char *bloops_track_str(bloopsatrack *);
# char *bloops_fxcmd_name(bloopsafxcmd fxcmd);
# float bloops_note_freq(char, int);
# char *bloops_sound_str(bloopsaphone *);
lib.bloops_track_str.argtypes = [POINTER(c_bloopsatrack)]
lib.bloops_track_str.restype = c_char_p
lib.bloops_fxcmd_name.argtypes = [c_int]
lib.bloops_fxcmd_name.restype = c_char_p
lib.bloops_note_freq.argtypes = [c_char, c_int]
lib.bloops_note_freq.restype = c_float
lib.bloops_sound_str.argtypes = [POINTER(c_bloopsaphone)]
lib.bloops_sound_str.restype = c_char_p

def test():
    B = lib.bloops_new()
    P = lib.bloops_square()
    track = lib.bloops_track2(B, P, c_char_p("a b c d e f g + a b c d e f"))
    lib.bloops_play(B)


