import {IconButton, InputAdornment, TextField} from "@mui/material";
import {useState} from "react";
import {Visibility, VisibilityOff} from "@material-ui/icons";

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
    const [showPassword, setShowPassword] = useState(false);

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
    const handleClickShowPassword = () => setShowPassword(!showPassword);
    const handleMouseDownPassword = () => setShowPassword(!showPassword);

    return (
        <>
            <TextField
                variant={"outlined"}
                fullWidth={true}
                sx={{width: "350px"}}
                type={showPassword ? 'text' : 'password'}
                placeholder={placeholder}
                value={password}
                onChange={setPassword}
                error={error}
                helperText={helperText}
                onBlur={checkPassword}
                InputProps={{
                    endAdornment: (
                        <InputAdornment position="end">
                            <IconButton
                                aria-label="toggle password visibility"
                                onClick={handleClickShowPassword}
                                onMouseDown={handleMouseDownPassword}
                            >
                                {showPassword ? <Visibility /> : <VisibilityOff />}
                            </IconButton>
                        </InputAdornment>
                    )
                }}
            />
        </>
    )
}

export default PasswordField;