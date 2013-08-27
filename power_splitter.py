L = 'l'
H = 'h'


class StateData(object):
    def __init__(self, state):
        self.state = state
        self.last_sample = 0
        self.num_samples = 0
        self.energy = 0

    def add(self, sample):
        self.energy += sample
        self.num_samples += 1

    def __repr__(self):
        return '%s\t %d\t %f\t %f' % (self.state,
                                self.num_samples,
                                self.energy,
                                self.energy/float(self.num_samples))

def main():
    with open('201306201120/power_1') as file:
        state_data = StateData(L)
        for line in file:
            current_sample = int(line.split()[1])
            if state_data.state == L and current_sample >= 500:
                print state_data
                state_data = StateData(H)
            elif state_data.state == H and current_sample <300:
                print state_data
                state_data = StateData(L)
            state_data.add(current_sample)
        print state_data


if __name__ == '__main__':
    main()
