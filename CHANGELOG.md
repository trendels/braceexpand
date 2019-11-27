# Changelog

## 0.1.5 (2019-11-27)

   - Don't pad int range when start or end is '-0'
   - Fix handling of range with increment '0'

## 0.1.4 (2019-11-26)

  - Add support for negative integers in ranges

## 0.1.3 (2019-10-02)

  - Fix bug where patterns nested inside an extra level of braces were not
    further expanded.

    For example, `{{a,b}}` now correctly expands to `{a} {b}`.

  - Drop support for Python 2.6

## 0.1.2 (2015-08-31)

  - Dont pad int range when start or end is '0'

## 0.1.1 (2015-01-10)

  - Updated list of supported Python versions

## 0.1 (2015-01-06)

  - Initial release
