#!/bin/#!/usr/bin/env bash

cut -d ' ' -f 1,2,3 | sed 's/>//g' | awk '{print $1, $2"_"$3}'
