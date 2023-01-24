# brewenv.py

A simple tool that enables immutable Linux distribution to install and use linuxbrew bottles without root privilege.

## Usage

Just download the `brewenv.py` and put it in your $PATH.

To install linuxbrew, please execute:

```
brewenv.py install
```

brewenv.py will create an environment with bwrap, which will utilize mount namespace to bin mount `/home/linuxbrew/.linuxbrew` inside it. And there will be no path like `/var/home` making brew confused.

And then you can enter the environment by executing:

```
brewenv.py exec
```
