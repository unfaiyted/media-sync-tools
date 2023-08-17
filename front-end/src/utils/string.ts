export function parseRGB(rgbString: string) : Array<number> {
    const matches = rgbString.match(/\d+/g); // match all groups of digits in the string

    if (matches && matches.length === 3) {
        return matches.map(Number); // convert each matched string to a number
    }

    console.error('Invalid RGB format');
    return [0,0,0];
}

export function camelCaseToWords(input: string): string {
    // Regular expression to match camel case pattern
    const camelCaseRegex = /([a-z])([A-Z])/g;

    // Replace camel case with space and capitalize
    const result = input.replace(camelCaseRegex, "$1 $2").replace(/\b\w/g, c => c.toUpperCase());

    return result;
}



