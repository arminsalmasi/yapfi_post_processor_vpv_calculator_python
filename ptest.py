import concurrent.futures


class ParallelTest:
    
    input = 0 
    zarib = 2

    def __init__(self,input):
        self.input = input

        
    def multiplier(self, param):
        r = self.zarib ** param
        return r

    def do_calc(self):
        results = []
        processes = 8
        with concurrent.futures.ProcessPoolExecutor(processes) as executor:
            for out in executor.map(self.multiplier, self.input):
                results.append(out)
        return results

def main():
    vect = range(1000)
    a = ParallelTest(vect)
    print(a.do_calc())


if __name__  == "__main__":
    main() 

