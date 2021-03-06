/*
 * encoder.c
 *
 *  Created on: 2020. dec. 20.
 *      Author: Norbert
 */

#include "encoder.h"

short is_long_pressed(GPIO_TypeDef* gpio_port, uint16_t button_pin, short polarity, uint16_t long_press){
	//In interrupt we cannot use HAL counter
	CoreDebug->DEMCR |= CoreDebug_DEMCR_TRCENA_Msk;
	//ITM->LAR = 0xC5ACCE55;
	DWT->CTRL |= 1 ; // enable the counter
	DWT->CYCCNT = 0; // reset the counter
	while(HAL_GPIO_ReadPin(gpio_port, button_pin) == polarity){
		__NOP();
		if(((DWT->CYCCNT/(SystemCoreClock/1000))> long_press)) return 1;
	}
	return 0;
}

uint32_t get_long_press_legth(GPIO_TypeDef* gpio_port, uint16_t button_pin){
	CoreDebug->DEMCR |= CoreDebug_DEMCR_TRCENA_Msk;
	//ITM->LAR = 0xC5ACCE55;
	DWT->CTRL |= 1 ; // enable the counter
	DWT->CYCCNT = 0; // reset the counter
	while(HAL_GPIO_ReadPin(gpio_port, button_pin) == 0){
			__NOP();
	}
	return DWT->CYCCNT/(SystemCoreClock/1000);
}

void snake_game_control(uint16_t GPIO_Pin){
	static uint32_t last_time;

	switch (GPIO_Pin){
	case ENCODER_PUSH_BUTTON_Pin:
		if (is_long_pressed(ENCODER_PUSH_BUTTON_GPIO_Port, ENCODER_PUSH_BUTTON_Pin, 0, LONG_PRESS)){
			temp_controller.menu = 1;
			snake_button(END); //END
			return;
		}
	case ENCODER_A_Pin:
		if(HAL_GPIO_ReadPin(ENCODER_B_GPIO_Port,ENCODER_B_Pin) && (HAL_GetTick()-last_time) > ROTARY_SLOW){
			last_time = HAL_GetTick();
			snake_button(RIGHT);
		}
	case ENCODER_B_Pin:
		if(HAL_GPIO_ReadPin(ENCODER_B_GPIO_Port,ENCODER_A_Pin) && (HAL_GetTick()-last_time) > ROTARY_SLOW)	{
			last_time = HAL_GetTick();
			snake_button(LEFT);
		}
	}
}

float *get_rotating_menu_item(temperature_controller_data* controller){
	if(controller->menu==1)	return	&controller->target_temp;
	if(controller->menu==2)	return	&controller->pid.Kp;
	if(controller->menu==3)	return	&controller->pid.Kd;
	if(controller->menu==4)	return	&controller->pid.Ki;
	if(controller->menu==5)	return	&controller->pid.max_P;
}

void rotate(int value, int* ptr){
	*ptr += value;
}

//Interrupt function called on button press
void encoder (uint16_t GPIO_Pin){
	HAL_NVIC_DisableIRQ(EXTI15_10_IRQn);
	if(temp_controller.menu == SNAKE_MENU) {					//snake game
		snake_game_control(GPIO_Pin);
		HAL_NVIC_EnableIRQ(EXTI15_10_IRQn);
		return;
	}
	static uint32_t last_time;
	float* ptr=get_rotating_menu_item(&temp_controller);

	switch(GPIO_Pin){
	case ENCODER_PUSH_BUTTON_Pin:
		if (temp_controller.menu == SET_DEFAULTS_MENU && is_long_pressed(ENCODER_PUSH_BUTTON_GPIO_Port, ENCODER_PUSH_BUTTON_Pin, 0, LONG_PRESS)){
			set_defaults();
			flash_WriteN(0, &temp_controller.target_temp,7,DATA_TYPE_64);
			last_time = HAL_GetTick();
			break;
		}
		if (is_long_pressed(ENCODER_PUSH_BUTTON_GPIO_Port, ENCODER_PUSH_BUTTON_Pin, 0, LONG_LONG_PRESS)){
			temp_controller.menu = SNAKE_MENU;
			last_time = HAL_GetTick();
			break;
		}

		if((HAL_GetTick()-last_time) > SHORT_PRESS)  temp_controller.menu++;
		if(temp_controller.menu > MENU_MAX-1) temp_controller.menu=1;
		last_time = HAL_GetTick();
		break;
	case ENCODER_A_Pin:
		if(HAL_GPIO_ReadPin(ENCODER_B_GPIO_Port,ENCODER_B_Pin))	{
			float change_slow=1;
			short change_fast=10;
			if(temp_controller.menu == SET_P_MENU) {
				change_slow=1;
				change_fast=2;
			}
			if(temp_controller.menu == SET_Kd_MENU) {
				change_slow=10;
				change_fast=100;
			}
			if(temp_controller.menu == SET_Ki_MENU) {
				change_slow=1;
				change_fast=1;
			}
			if((HAL_GetTick()-last_time) > ROTARY_SLOW)			rotate(-change_slow,ptr);
			else if((HAL_GetTick()-last_time) > ROTARY_FAST)	rotate(-change_fast,ptr);
			else												break;
			temp_controller.defaults = 0;
			flash_WriteN(0, &temp_controller.target_temp,7,DATA_TYPE_64);
			last_time = HAL_GetTick();
		}
		break;
	case ENCODER_B_Pin:
		if(HAL_GPIO_ReadPin(ENCODER_B_GPIO_Port,ENCODER_A_Pin))	{
			float change_slow=1;
			short change_fast=10;
			if(temp_controller.menu == SET_P_MENU) {
				change_slow=1;
				change_fast=2;
			}
			if(temp_controller.menu == SET_Kd_MENU) {
				change_slow=10;
				change_fast=100;
			}
			if(temp_controller.menu == SET_Ki_MENU) {
				change_slow=1;
				change_fast=1;
			}
			if((HAL_GetTick()-last_time) > ROTARY_SLOW)			rotate(change_slow,ptr);
			else if((HAL_GetTick()-last_time) > ROTARY_FAST)	rotate(change_fast,ptr);
			else												break;
			temp_controller.defaults = 0;
			flash_WriteN(0, &temp_controller.target_temp,7,DATA_TYPE_64);
			last_time = HAL_GetTick();
		}
		break;
	}
	HAL_NVIC_EnableIRQ(EXTI15_10_IRQn);
}
