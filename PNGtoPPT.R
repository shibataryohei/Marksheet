library(tidyverse)

PATH <- "/Users/Ryohei/Dropbox/Presentation/2019/190523_JSPS_Marksheet/Slide_JSPS2019_Marksheet" # PNGファイルのディレクトリ

# 
setwd(PATH) 
dir() %>% 
  file.rename(., gsub("(?<![0-9])([0-9])(?![0-9])",
                      "0\\1",
                      .,
                      perl = TRUE)) %>% # Slide1 -> Slide01
  
setwd(PATH) 
dir() %>%
  paste0("![](",PATH,"/", ., ")") %>%
  noquote %>% # patse()の結果から"を除去する
  cat(., sep="\n\n") # \nは改行を表す
