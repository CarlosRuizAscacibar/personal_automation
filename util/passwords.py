import pykeepass
import os

def open_vault():
    p = os.path.dirname(os.path.realpath(__file__))
    # password is in a file inside computer and service
    vault_pass = open(p + '/../pass.txt', 'r', encoding='utf-8').readline().strip()
    vault = pykeepass.PyKeePass(p + '/../vault.kdbx', password=vault_pass)
    return vault


def get_entry(title):
    vault = open_vault()
    # collect passwords from kdbx
    return [x for x in vault.entries if x.title == title][0]
