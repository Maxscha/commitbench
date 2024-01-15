from collections import Counter

f = open('resources/repos.txt')

l = f.readlines()

orgas = [line.split('/')[0] for line in l]

print(f'Number of repositories: {len(l)}')


print(f'Number of organisations: {len(list(set(orgas)))}')

c = Counter(orgas)


print(f'Max: {c.most_common(1)}')
print(f'Mean: {c.most_common(int(len(c)/2))[-1]}')

print(f'Average: {len(l) / len(c)}')


# How many organisations are in the top 10% of repositories?

print(sum([count for user, count in c.most_common(int(len(c)/10))]))