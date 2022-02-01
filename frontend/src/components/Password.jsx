import {TextField} from "@mui/material";
import {useState} from "react";

const errorText = 'Passwords must contain a capital letter, a digit and be between 8 to 14 characters.'
const defaultText = 'You can enter numbers, letters and special characters'


// https://stackoverflow.com/questions/43993008/regex-for-validate-password-in-reactjs
const validatePassword = (password) => {
    const re = {
        'capital': /[A-Z]/,
        'digit': /[0-9]/,
        'full': /^[A-Za-z0-9]{7,13}$/
    };
    return re.capital .test(password) &&
        re.digit   .test(password) &&
        re.full    .test(password);
}

const PasswordField = ({placeholder, password, setPassword}) => {
    const [error, setError] = useState(false);
    const [helperText, setHelperText] = useState(defaultText);

    const checkPassword = (event) => {
        const password = event.target.value;
        if (!validatePassword(password)) {
            setError(true)
            setHelperText(errorText)
        } else {
            setError(false)
            setHelperText(defaultText)
        }
    }

    return (
        <>
            <TextField
                variant={"outlined"}
                fullWidth={true}
                sx={{width: "350px"}}
                type={'password'}
                placeholder={placeholder}
                value={password}
                onChange={setPassword}
                error={error}
                helperText={helperText}
                onBlur={checkPassword}
            />
        </>
    )
}

export default PasswordField;