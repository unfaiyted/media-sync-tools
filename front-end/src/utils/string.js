export function parseRGB(rgbString) {
    const matches = rgbString.match(/\d+/g); // match all groups of digits in the string

    if (matches && matches.length === 3) {
        return matches.map(Number); // convert each matched string to a number
    }

    console.error('Invalid RGB format');
    return [0,0,0];
}
