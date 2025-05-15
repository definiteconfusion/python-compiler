fn o_type<T>(t: &T) -> String {
    std::any::type_name::<T>().to_string()
}

fn main() {
    let mut name = "Kevin";
    let mut age = 30;
    let mut age1 = age + 1;
    let mut type_of_name = o_type(&name);
    println!("{} {}", age, name);
}
