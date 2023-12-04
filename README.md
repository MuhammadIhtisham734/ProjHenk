# ProjHenk
Data...

### Prepare data, I mentioned some cleaning needs below. Some more u should find and add to list also

#### Yelp Dataset
- [x] Remove duplicate entries (Places with the same values in the `NAME` and `ADDRESS` fields)
- [x] Remove restaurants with "review of" in their name
- [ ] Fix special characters
  - We replace Apostrophes and "ü", but there are still characters missing
- [ ] Remove entries with numbers instead of names.
- [ ] Fix places containing a '-' in their name only contain characters before the '-' sign as name value.
  - e.g. "Pi-Hi Cafe" -> "Pi"
- [x] Remove places sharing the same phone number.
  - e.g. 149 entries with the value of "1445980000000" in the Yelp dataset.
- [ ] Replace special characters in phone numbers.
  - Not sure if we need to do this?
- [ ] Fix NaN values in ratings.
- [x] Trim restaurant names.
- [x] Remove places with missing address parts, e.g. no street name

#### Zomato Dataset
- [x] Trim restaurant names.

# Notes
* Some places names are indeed simply their address in the yelp dataset. Weird.
