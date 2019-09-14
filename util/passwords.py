import pykeepass


def open_vault():
    # password is in a file inside computer and service
    vault_pass = open('pass.txt', 'r', encoding='utf-8').readline()
    vault = pykeepass.PyKeePass('vault.kdbx', password=vault_pass)
    return vault


def get_entry(title):
    vault = open_vault()
    # collect passwords from kdbx
    return [x for x in vault.entries if x.title == title][0]
