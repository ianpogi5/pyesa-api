#!/bin/bash

aws cloudfront create-invalidation --distribution-id E1GXPGZPJROQX7 --paths "/api/*" --profile pyesa