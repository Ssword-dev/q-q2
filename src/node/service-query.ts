// const $0 = 48;
// const A = 65;
// const X = 88;
// const Z = 90;
// const _ = 95;
// const a = 97;
// const x = 120;
// const z = 122;

// const StringFromCharCode = (ccs: number[]) =>
//   String.fromCharCode.apply(String.fromCharCode, ccs);

// function parseQuery(query: string) {
//   let idx = 0;

//   function peekCC(offset = 0) {
//     return query.charCodeAt(idx + 0);
//   }

//   function next() {
//     return query[idx++];
//   }

//   function nextCC() {
//     return query.charCodeAt(idx++);
//   }

//   function parseIdentifier() {
//     let cc = peekCC();
//     let buffer = [];

//     while ((a <= cc && cc <= z) || (A <= cc && cc <= Z) || cc === _) {
//       buffer.push(cc);
//       idx++;
//     }

//     return StringFromCharCode(buffer);
//   }

//   function parseHex() {}

//   function parseNumber(): number {
//     const nextCC = peekCC();
//     const probablyX = peekCC(1);

//     if (nextCC === $0 && probablyX === x) {
//       idx += 2;
//       return parseHex();
//     }

//     let acc = 0;
//   }
// }
