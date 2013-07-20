# -*- coding: utf-8 -*-

import sys
from bot import bot

if __name__ == "__main__":
    if len(sys.argv)>1 and sys.argv[1] == 'testing':
        from config import TestConfig
        bot.set_config(TestConfig())
    elif len(sys.argv)>1 and sys.argv[1] == 'ceci':
        from config import CeciConfig
        bot.set_config(CeciConfig())
    elif len(sys.argv)>1 and sys.argv[1] == 'freenode':
        from config import EntchenConfigFreenode
        bot.set_config(EntchenConfigFreenode())
    else:
        from config import EntchenConfig
        bot.set_config(EntchenConfig())

    bot.run()
