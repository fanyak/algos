function subSets(a: number[], res:number[][]): number[][] {

    if(!a.length) {
        res.push([])
        return res;
    }

    const [first, ...rest] = a;
    const n = res.map((s: number[]) => s.concat(first))
    res.push([first], ...n);

    return subSets(rest, res);

}


const list = [1,2,3,4];

console.log(subSets(list, []))