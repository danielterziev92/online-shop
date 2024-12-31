const errorMessages: Record<string, string> = {
    'This password is too common.': 'Тази парола е твърде разпространена.',
    'Password must contain uppercase letter.': 'Паролата трябва да съдържа главна буква.',
    'Invalid credentials': 'Невалидни данни',
    'Code does not exist': 'Въвели сте несъществуващ код.'
};

export const formatErrorMessage = (error: string): string[] => {
    try {
        const errorArray: string[] = JSON.parse(error.replace(/'/g, '"'));
        return errorArray.map(msg => errorMessages[msg] || msg);
    } catch {
        return [errorMessages[error] || error];
    }
}