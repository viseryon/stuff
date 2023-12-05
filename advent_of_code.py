import re


with open("input.txt", "r") as f:
    file = f.read()
    file = file.split("\n\n")

# seed -> soil -> fertilizer -> water -> light -> temperature -> humidity -> location

destination_names = []
for i, mapp in enumerate(file):
    if i == 0:
        seeds = re.findall(r"\d+", mapp)
        seeds = [int(num) for num in seeds]

        seeds_starts, seeds_lengths = [], []

        for see, seed in enumerate(seeds):
            if see % 2 == 0:
                seeds_starts.append(seed)
            else:
                seeds_lengths.append(seed)

        seeds_set = set()
        for seed_start, seed_length in zip(seeds_starts, seeds_lengths):
            temp = set(range(seed_start, seed_start+seed_length))
            seeds_set = seeds_set.union(temp)

        seeds = list(seeds_set)
        print(seeds, 'seeds')
        continue

    destinations, sources = [], []

    for j, line in enumerate(mapp.split("\n")):
        if j == 0:
            line = line.split("-to-")
            destination_name = line[1].removesuffix(" map:")
            destination_names.append(destination_name)
            continue

        nums = re.findall(r"\d+", line)
        nums = [int(num) for num in nums]
        destination, source, length = nums

        destination_range = (destination, destination + length)
        source_range = (source, source + length)

        destinations.append(destination_range)
        sources.append(source_range)

    for s, seed in enumerate(seeds):
        for (dist_start, dist_end), (sour_start, sour_end) in zip(destinations, sources):

            if not (seed < sour_end and seed >= sour_start):
                continue
            
            seed += dist_start - sour_start
            seeds[s] = seed
            break


    print(seeds, destination_name)

print(min(seeds))

